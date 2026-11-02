"""orph.py: split orphan instrs (no owner fn) into REAL clusters (target of a branch/call from owned code, or from jump table) vs JUNK (clear to data). Out: orph_real.txt (cluster starts), orph_junk.txt (addresses)."""
import re,collections
own={};ins={}
for l in open('instr.tsv'):
    a,n,o=l.split();a=int(a,16);own[a]=o;ins[a]=int(n)
orph=sorted(a for a in own if own[a]=='-')
cl=[]
for a in orph:
    if cl and a-cl[-1][-1]<=12: cl[-1].append(a)
    else: cl.append([a])
tgt=collections.defaultdict(list)
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +[0-9a-f]{8}(?: +[0-9a-f]{8})? +(\S+)\s+.*?0x([0-9a-f]+)\s*$',l)
    if m and m.group(2).startswith(('b','c','call')) :
        s=int(m.group(1),16);t=int(m.group(3),16)
        if s in own and own[s]!='-': tgt[t].append(s)
for l in open('jtab.tsv'):
    p=l.split('\t')
    for t in p[4].strip().split(','): tgt[int(t,16)].append(int(p[0],16))
real=[];junk=[]
for c in cl:
    s=set(c)
    if any(t in s or any(x<=t<=x+4 for x in c) for t in tgt if c[0]-4<=t<=c[-1]+4) and any(own.get(x)!='-' for t in tgt if c[0]<=t<=c[-1] for x in tgt[t]):
        real.append(c)
    else: junk+=c
print(len(cl),'clusters; real',len(real),'junk instrs',len(junk))
print(' '.join('%x(%d)'%(c[0],len(c)) for c in real))
open('orph_real.txt','w').write(''.join('%x\n'%c[0] for c in real))
open('orph_junk.txt','w').write(''.join('%x\n'%a for a in junk))
