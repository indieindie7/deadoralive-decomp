"""gapclass.py: classify the uncovered-ret seeds (seeds2.txt) by evidence: branch xref from covered code, ROM pointer word, or none."""
import re, struct, collections
d=open('prog.bin','rb').read()
cov=set()
for l in open('funcinfo_doaarc.tsv'):
    p=l.split()
    if p and p[0]=='F':
        a=int(p[1],16);cov.update(range(a,a+int(p[4])))
words=collections.defaultdict(list)
for i in range(0,len(d)-3,4):
    w=struct.unpack_from('<I',d,i)[0]
    words[w].append(i)
bt=collections.defaultdict(list)   # branch target -> srcs
for l in open('prog.dis'):
    m=re.match(r'([0-9a-f]+): +\S+(?: +\S+)? +(b|bal|call|callx|balx|bx|be|bne|bg|bge|bl|ble|bo|bno|bno|cmpibe|cmpibne|cmpibg|cmpibge|cmpibl|cmpible|cmpobe|cmpobne|cmpobg|cmpobge|cmpobl|cmpoble|bbs|bbc|b[a-z]*)\s+.*?0x([0-9a-f]+)\s*$',l)
    if m: bt[int(m.group(3),16)].append(int(m.group(1),16))
out=[]
for s in open('seeds2.txt'):
    a=int(s,16)
    br=[x for x in bt.get(a,[]) if x in cov]
    pt=[x for x in words.get(a,[]) if x not in cov or True]
    out.append((a,len(br),len(pt)))
n=collections.Counter(('br' if b else '')+('pt' if p else '') or 'none' for a,b,p in out)
print(n)
open('gapclass.tsv','w').write(''.join('%x\t%d\t%d\n'%o for o in out))
