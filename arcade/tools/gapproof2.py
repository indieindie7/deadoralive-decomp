"""gapproof2.py: refine OPEN rets: PAD (word 0x0a000000 with undecodable/ret/covered-fn-end neighbour, no xref), JUNK (>=2 undecodable words within +-3), else REVIEW."""
import re,collections
cov=set()
for l in open('funcinfo_doaarc.tsv'):
    p=l.split()
    if p and p[0]=='F':
        a=int(p[1],16);cov.update(range(a,a+int(p[4])))
rows=[]
for l in open('prog.dis'):
    m=re.match(r'([0-9a-f]+): +([0-9a-f]{8})(?: +[0-9a-f]{8})? +(\S+)',l)
    if m: rows.append((int(m.group(1),16),m.group(3),m.group(2)))
idx={a:i for i,(a,_,_) in enumerate(rows)}
cl={}
for l in open('gapclass.tsv'):
    a,b,p=l.split();cl[int(a,16)]=(int(b),int(p))
res=collections.OrderedDict();c=collections.Counter()
for l in open('gapproof.tsv'):
    r,k,w=(l.rstrip('\n').split('\t')+[''])[:3]
    r=int(r,16)
    if k=='DATA': res[r]=('DATA',w);c['DATA']+=1;continue
    i=idx[r];nb=rows[max(0,i-3):i]+rows[i+1:i+4]
    q=sum(1 for x in nb if x[1]=='?')
    if rows[i][2]=='0a000000' and q>=1: k='PAD'
    elif q>=2: k='JUNK'
    else: k='REVIEW'
    c[k]+=1;res[r]=(k,'')
print(c)
open('gapproof2.tsv','w').write(''.join('%x\t%s\t%s\n'%(r,k,w) for r,(k,w) in res.items()))
print(' '.join('%x'%r for r,(k,w) in res.items() if k=='REVIEW'))
