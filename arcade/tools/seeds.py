"""seeds.py <out>: function seeds from prog.dis call/callx/bal/balx targets inside ROM (no RAM-code copy in DOA)."""
import re, sys
seeds = {0x410, 0x5f0}
for l in open('ghidra/prog.dis'):
    m = re.match(r'([0-9a-f]+): .*?\b(call|callx|bal|balx)\s+(0x[0-9a-f]+)\s*$', l)
    if not m: continue
    t = int(m.group(3), 16)
    if 0x400 <= t < 0x100000 and t % 4 == 0: seeds.add(t)
open(sys.argv[1], 'w').write(''.join('0x%08x\n' % s for s in sorted(seeds)))
print(len(seeds))
