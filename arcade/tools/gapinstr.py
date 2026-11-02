"""gapinstr.py: coverage by Ghidra instruction (instr.tsv), not function body. Reports: rets with no instruction (classified DATA/PAD/JUNK/REVIEW by gapproof rules), orphan instructions (no owner fn)."""
import re,collections
ins={};orph=[]
for l in open('instr.tsv'):
    a,n,o=l.split();a=int(a,16);ins[a]=int(n)
    if o=='-': orph.append(a)
covb=set()
for a,n in ins.items(): covb.update(range(a,a+n))
rows=[]
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +([0-9a-f]{8})(?: +[0-9a-f]{8})? +(\S+)',l)
    if m: rows.append((int(m.group(1),16),m.group(3),m.group(2)))
idx={a:i for i,(a,_,_) in enumerate(rows)}
refs=set()
for l in open('prog.dis'):
    m=re.search(r'\b(?:lda|ld|ldob|ldos|ldib|ldis|ldl|ldt|ldq|st|stob|stos|stl)\s+0x([0-9a-f]+)',l)
    if m:
        v=int(m.group(1),16)
        if 0x400<=v<0x100000: refs.add(v)
import bisect
refs=sorted(refs)
c=collections.Counter();rev=[]
for a,o,w in rows:
    if o!='ret' or not 0x400<=a<0x100000 or a in ins: continue
    i=idx[a];nb=rows[max(0,i-3):i]+rows[i+1:i+4]
    q=sum(1 for x in nb if x[1]=='?')
    j=bisect.bisect_right(refs,a)-1
    dataref=j>=0 and all(x not in covb for x in range(refs[j],a+1,4))
    if dataref: k='DATA'
    elif w=='0a000000' and q>=1: k='PAD'
    elif q>=2: k='JUNK'
    else: k='REVIEW';rev.append(a)
    c[k]+=1
print(c,'orphan instr',len(orph))
print('REVIEW',' '.join('%x'%a for a in rev))
open('gapinstr_review.txt','w').write(''.join('%x\n'%a for a in rev))
print('orph',' '.join('%x'%a for a in orph[:60]))
