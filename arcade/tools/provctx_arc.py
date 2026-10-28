# provctx_arc.py: review contexts for every provisional name of the DOA Model 2A arcade program.
# Body of each provisional function + up to 2 caller bodies (from funcinfo C lines), split into N files.
# usage: py -3.13 -I provctx_arc.py <ghidra dir> <N> <out prefix>
import sys, os, re
g, n, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]
body = {}; cur = None
for l in open(os.path.join(g, 'decomp_doaarc.c'), encoding='utf-8', errors='replace'):
    m = re.match(r'// ==== (\S+) @ ([0-9a-f]{8})', l)
    if m: cur = m.group(2); body[cur] = [l]
    elif cur: body[cur].append(l)
callers = {}; f = None
for l in open(os.path.join(g, 'funcinfo_doaarc.tsv'), encoding='utf-8'):
    p = l.split()
    if not p: continue
    if p[0] == 'F': f = p[1]
    elif p[0] == 'C' and f: callers.setdefault(p[1], []).append(f)
prov = [l.split()[0][2:] for l in open(os.path.join(g, 'hand_doaarc.txt'), encoding='utf-8')
        if re.match(r'0x\S+ func \S+ (hand )?provisional', l)]
items = []
for a in prov:
    t = ['#### ITEM 0x' + a + '\n'] + body.get(a, ['(no body)\n'])[:150]
    for c in callers.get(a, [])[:2]:
        t += ['---- caller\n'] + body.get(c, [])[:80]
    items.append(''.join(t))
k = (len(items) + n - 1) // n
for i in range(n):
    open(f'{pre}{i+1}.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(items[i*k:(i+1)*k]))
print('items', len(items), 'per file', k)
