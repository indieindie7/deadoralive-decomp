"""jtab.py: jump tables = `ld T[gN*4],gM ; bx (gM)`; count from preceding `cmpobl N,..` (N+1 entries). Out: jtab.tsv bx_addr table count status; targets must be 4-aligned ROM code (decodable, not '?')."""
import re,struct
d=open('prog.bin','rb').read()
rows=[]
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +([0-9a-f]{8})(?: +([0-9a-f]{8}))? +(\S+)\s*(.*)',l)
    if m: rows.append((int(m.group(1),16),m.group(4),m.group(5).strip()))
mn={a:(o,r) for a,o,r in rows}
out=[];bad=[]
for i,(a,o,r) in enumerate(rows):
    if o!='bx' or not r.startswith('('): continue
    reg=r.strip('()')
    # previous instr must be ld T[x*4],reg
    p=rows[i-1]
    m=re.match(r'0x([0-9a-f]+)\[(\w+)\*4\],(\w+)',p[2]) if p[1]=='ld' else None
    if not m or m.group(3)!=reg: continue
    T=int(m.group(1),16);ix=m.group(2)
    N=None
    for q in rows[max(0,i-5):i-1]:
        mm=re.match(r'(cmpobl|cmpobg|cmpibl|cmpibg)\s+(\d+),'+ix+r',',q[1]+' '+q[2]) 
        if q[1] in('cmpobl','cmpibl'):
            mm=re.match(r'(\d+),'+ix+',',q[2])
            if mm: N=int(mm.group(1))
    if N is None:
        ts=[];k=0
        while True:
            t=struct.unpack_from('<I',d,T+4*k)[0]
            if not(0x400<=t<0x100000 and t%4==0 and t in mn and mn[t][0]!='?'): break
            ts.append(t);k+=1
        N=len(ts)-1;bad.append((a,T,N+1))
    else:
        ts=[struct.unpack_from('<I',d,T+4*k)[0] for k in range(N+1)]
    ok=all(0x400<=t<0x100000 and t%4==0 and t in mn and mn[t][0]!='?' for t in ts)
    out.append((a,T,N+1,'ok' if ok else 'bad',ts))
print(len(out),'tables',sum(1 for o in out if o[3]=='ok'),'ok',len(bad),'nobound',[(hex(a),hex(t)) for a,t,_ in bad])
for o in out:
    if o[3]!='ok': print('BAD',hex(o[0]),hex(o[1]),o[2],[hex(t) for t in o[4]][:6])
open('jtab.tsv','w').write(''.join('%x\t%x\t%d\t%s\t%s\n'%(a,T,n,s,','.join('%x'%t for t in ts)) for a,T,n,s,ts in out))
