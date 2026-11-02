"""ramtab.py: every work-RAM (0x500000-0x5fffff) address used as an instruction operand. Types from access width (ldob/stob=1,ldos=2,ld=4,ldl=8,ldt=12,ldq=16); lda = address taken; [reg*n]/(reg) = indexed. Out: ramtab.tsv addr widths(set) idx_scales reads writes lda_count nfn topfns"""
import re,collections
own={}
for l in open('instr.tsv'):
    a,n,o=l.split();own[int(a,16)]=o
names={}
for l in open('funcinfo_doaarc.tsv'):
    p=l.split()
    if p and p[0]=='F': names[int(p[1],16)]=p[2]
W={'ldob':1,'ldib':1,'stob':1,'stib':1,'ldos':2,'ldis':2,'stos':2,'stis':2,'ld':4,'st':4,'ldl':8,'stl':8,'ldt':12,'stt':12,'ldq':16,'stq':16}
T=collections.defaultdict(lambda:{'w':collections.Counter(),'ix':collections.Counter(),'r':0,'w_':0,'lda':0,'fn':collections.Counter(),'reg':0,'ctx':set()})
pat=re.compile(r'^\s*([0-9a-f]+): +[0-9a-f]{8} +[0-9a-f]{8} +(\w+)\s+(.*)$')
for l in open('prog.dis'):
    m=pat.match(l)
    if not m: continue
    pc=int(m.group(1),16);op=m.group(2);args=m.group(3)
    for mm in re.finditer(r'0x([0-9a-f]+)(\((\w+)\)|\[(\w+)\*(\d)\])?',args):
        v=int(mm.group(1),16)
        if not 0x500000<=v<0x600000: continue
        t=T[v];fn=own.get(pc,'-')
        t['fn'][fn]+=1
        if op in W:
            t['w'][W[op]]+=1
            if op.startswith('ld'): t['r']+=1
            else: t['w_']+=1
        elif op=='lda': t['lda']+=1
        if mm.group(4): t['ix'][int(mm.group(5))]+=1
        elif mm.group(3): t['reg']+=1
rows=[]
for v in sorted(T):
    t=T[v]
    rows.append('%x\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%s'%(v,','.join('%d:%d'%x for x in sorted(t['w'].items())),','.join('%d:%d'%x for x in sorted(t['ix'].items())),t['r'],t['w_'],t['lda'],t['reg'],len(t['fn']),','.join(names.get(int(f,16),f) if f!='-' else '-' for f,_ in t['fn'].most_common(3))))
open('ramtab.tsv','w').write('\n'.join(rows)+'\n')
print(len(T),'distinct RAM operand addresses')
