"""holes.py: dis-decodable instruction rows inside a function's [min,max] instruction extent that Ghidra has no instruction for (missed code). Out holes.tsv: addr ownerfn"""
import re,collections
ins={};ext={}
for l in open('instr.tsv'):
    a,n,o=l.split();a=int(a,16);ins[a]=int(n)
    lo,hi=ext.get(o,(a,a));ext[o]=(min(lo,a),max(hi,a))
ranges=sorted((lo,hi,o) for o,(lo,hi) in ext.items() if o!='-')
import bisect
los=[r[0] for r in ranges]
cov=set()
for a,n in ins.items(): cov.update(range(a,a+n))
holes=[]
jt=set()
for l in open('jtab.tsv'):
    p=l.split('\t');T=int(p[1],16)
    jt.update(range(T,T+4*int(p[2])))
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +([0-9a-f]{8})(?: +[0-9a-f]{8})? +(\S+)',l)
    if not m: continue
    a=int(m.group(1),16)
    if a in cov or a in jt or m.group(3)=='?' or a<0x400: continue
    i=bisect.bisect_right(los,a)-1
    if i>=0 and ranges[i][0]<=a<=ranges[i][1]:
        holes.append((a,ranges[i][2],m.group(3),m.group(2)))
print(len(holes),'holes')
cl=[]
for h in holes:
    if cl and h[0]-cl[-1][-1][0]<=8 and h[1]==cl[-1][-1][1]: cl[-1].append(h)
    else: cl.append([h])
print(len(cl),'clusters')
open('holes.tsv','w').write(''.join('%x\t%s\t%s\t%s\n'%h for h in holes))
big=sorted(cl,key=lambda c:-len(c))[:15]
print([(hex(c[0][0]),len(c),c[0][1]) for c in big])
