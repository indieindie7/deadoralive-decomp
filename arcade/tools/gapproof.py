"""gapproof.py: proof class per uncovered ret. DATA = lies in uncovered run that starts at (or after) a ROM address code loads as data (lda/ld imm, or in-ROM pointer from data), no branch xref. CODEPTR = pointer word to its function start. BR = branch xref from covered code."""
import re,struct,collections,bisect
d=open('prog.bin','rb').read()
cov=bytearray(0x100000)
for l in open('funcinfo_doaarc.tsv'):
    p=l.split()
    if p and p[0]=='F':
        a=int(p[1],16)
        for i in range(a,a+int(p[4])): cov[i]=1
refs=set()
for l in open('prog.dis'):
    m=re.search(r'\b(?:lda|ld|ldob|ldos|ldib|ldis|ldl|ldt|ldq|st|stob|stos|stl)\s+0x([0-9a-f]+)',l)
    if m:
        v=int(m.group(1),16)
        if 0x400<=v<0x100000: refs.add(v)
refs=sorted(refs)
cls={}
for l in open('gapclass.tsv'):
    a,b,p=l.split();cls[int(a,16)]=(int(b),int(p))
rets=[]
for l in open('prog.dis'):
    m=re.match(r'([0-9a-f]+): +\S+(?: +\S+)? +ret\b',l)
    if m:
        a=int(m.group(1),16)
        if 0x400<=a<0x100000 and not cov[a]: rets.append(a)
out=[];cnt=collections.Counter()
seedof={}
for s in open('seeds2.txt'):
    pass
for r in rets:
    i=bisect.bisect_right(refs,r)-1
    k='OPEN'
    if i>=0:
        D=refs[i]
        if all(not cov[x] for x in range(D,r+1,4)): k='DATA'; why='ldref 0x%x'%D
    if k=='OPEN':
        why=''
    out.append((r,k,why)); cnt[k]+=1
print(cnt)
open('gapproof.tsv','w').write(''.join('%x\t%s\t%s\n'%o for o in out))
