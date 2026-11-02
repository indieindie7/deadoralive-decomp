"""gapdata.py: for each uncovered ret decide DATA (undecodable '?' words / ret-runs near it, no branch/pointer xref) vs CODE-candidate."""
import re,collections
cov=set()
for l in open('funcinfo_doaarc.tsv'):
    p=l.split()
    if p and p[0]=='F':
        a=int(p[1],16);cov.update(range(a,a+int(p[4])))
rows=[]
for l in open('prog.dis'):
    m=re.match(r'([0-9a-f]+): +(\S+)(?: +\S+)? +(\S+)',l)
    if m: rows.append((int(m.group(1),16),m.group(3),m.group(2)))
idx={a:i for i,(a,_,_) in enumerate(rows)}
cls={}
for l in open('gapclass.tsv'):
    a,b,p=l.split();cls[int(a,16)]=(int(b),int(p))
miss=[a for a,o,_ in rows if 0x400<=a<0x100000 and o=='ret' and a not in cov]
res=[]
for r in miss:
    i=idx[r]
    w=rows[max(0,i-12):i+13]
    q=sum(1 for x in w if x[1]=='?')
    rr=sum(1 for x in w if x[1]=='ret')
    unc=sum(1 for x in w if x[0] not in cov)
    res.append((r,q,rr,unc))
data=[x for x in res if x[1]>=2 or x[2]>=3]
code=[x for x in res if not(x[1]>=2 or x[2]>=3)]
print(len(miss),'data',len(data),'code-cand',len(code))
open('gapcode.tsv','w').write(''.join('%x\t%d\t%d\t%d\n'%x for x in code))
print([hex(x[0]) for x in code])
