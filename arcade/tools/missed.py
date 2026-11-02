"""missed.py: branch/call targets from Ghidra-owned instructions that Ghidra has no instruction at, and dis decodes as an instruction. Out missed.tsv: src target."""
import re
own={};ins=set()
for l in open('instr.tsv'):
    a,n,o=l.split();a=int(a,16);own[a]=o;ins.add(a)
valid=set()
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +[0-9a-f]{8}(?: +[0-9a-f]{8})? +(\S+)',l)
    if m and m.group(2)!='?': valid.add(int(m.group(1),16))
out=[]
for l in open('prog.dis'):
    m=re.match(r'\s*([0-9a-f]+): +[0-9a-f]{8}(?: +[0-9a-f]{8})? +(\S+)\s+.*?0x([0-9a-f]+)\s*$',l)
    if not m or not m.group(2).startswith(('b','c','call','bal')): continue
    s=int(m.group(1),16);t=int(m.group(3),16)
    if s in own and own[s]!='-' and t not in ins and t in valid and 0x400<=t<0x100000 and t%4==0 and s!=t:
        if m.group(2) in('bal','balx','call','callx','b','bno','bo','be','bne','bg','bge','bl','ble') or m.group(2).startswith(('cmp','bb')):
            out.append((s,t))
print(len(out),'missed branch targets',len({t for s,t in out}),'distinct')
open('missed.tsv','w').write(''.join('%x\t%x\n'%o for o in out))
