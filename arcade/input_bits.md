# DOA arcade input byte 0x54fccd (P1) / 0x54fcce (P2) - bit map (r8, 11-02)

## Raw source (prog.dis 08148..081b0, io_ReadAllInputs 0x8050)
`ldos 0x1c00004` -> `stob 0x54fccd` (08160..08174); `ldos 0x1c00006` -> `stob 0x54fcce` (0817c..08184); port 0x1c00002 -> 0x54fccc (system), 0x1c00008 -> 0x54fccf (unread). Low byte of each 16-bit port read is kept. Then `ld (g6=0x54fccc)` / `not` / `st` (081a8..081b0): whole dword inverted, so hardware active-low -> RAM active-high (1 = pressed). Edges: 0x54fcd4 = new & ~prev (081b4), 0x54fcd8 = prev & ~new (081c0); prev copy 0x54fcd0 (08154). These are the ONLY stores to 0x54fccc..cf in prog.dis (grep all `st*` + all 4-byte address constants in prog.bin: every other ref is a load).

## Bit table
| bit | mask | meaning | raw source | live evidence (hidden copy of frozen build, run IN) | AI evidence |
|---|---|---|---|---|---|
| 0 | 0x01 | HOLD (button F, guard/hold) | port byte bit0 (active low) | p1_hold -> 0x54fccd=0x01 f2701-2706; p2_hold -> 0x54fcce=0x01 f2821-2826 | script operand low nibble 1 (IN(1)); ring R 0x563f90+p*0x80 copy (25ef0) |
| 1 | 0x02 | PUNCH (P) | bit1 | p1_punch 0x02 f2713-18; p2_punch 0x02 f2833-38 | IN(2) |
| 2 | 0x04 | KICK (K) | bit2 | p1_kick 0x04 f2725-30; p2_kick 0x04 f2845-50 | IN(4) |
| 3 | 0x08 | UNUSED. No code tests it alone; only full-byte compares (operand bit8: IN(180),IN(380),IN(140),IN(110),IN(120)) include it, where it must read 0 | bit3 of port byte; harness has no key for it (nb[3]=nullptr in m2doa/doa_app main.cpp), so never pressable | all-7-buttons combo = 0xf7 (f2809, p2 f2905): bit3 stays 0; never seen set in 250 dumped frames | no operand uses low-nibble bit 8 (move_table.tsv) |
| 4 | 0x10 | DOWN | bit4 | p1_down 0x10 f2749-54; p2_down 0x10 f2869-74 | high nibble 0x10 (IN(310)=held DOWN) |
| 5 | 0x20 | UP | bit5 | p1_up 0x20 f2737-42; p2_up 0x20 f2857-62 | 0x20 |
| 6 | 0x40 | RIGHT (screen) | bit6 | p1_right 0x40 f2773-78; p2_right 0x40 f2893-98 | 0x40; swapped with 0x80 when mirror flag 0x5645e6[p]==1 (ai_OpSwapInputBits 28d50) |
| 7 | 0x80 | LEFT (screen) | bit7 | p1_left 0x80 f2761-66; p2_left 0x80 f2881-86 | 0x80 (guard: (byte&0xf0)==0x80 / 0x90) |

Combos: punch+kick = 0x06 (f2785), hold+punch+kick = 0x07 (f2797), all seven buttons = 0xf7 (f2809). Frame numbering: byte becomes visible in the dump 1 frame after the script frame; 0x54fcd5 (P1 press edge) is set for exactly 1 frame, 0x54fcd1 (prev) follows 1 frame later, 0x54fcd9 release edge 1 frame after release.
Other readers of the byte: 04854/04868 `and 7 ==7` (all three buttons held, P1/P2), 04ab0 bit0, 04b54 bit2, 17548..17588 and 17854/17888 bits 0-2, 6f3c0 bbc 0, ring copy 25ef0.

## AI / CPU fighter (PREMISE CHECK: the CPU does NOT write these bits)
- Nothing but io_ReadAllInputs writes 0x54fccd/0x54fcce (see above). The CPU fighter (fighter+0x00 'mancom'==0) has NO input byte of its own: the history-ring writer (25ef0..25f98) copies 0x54fccd[slot] for every slot unconditionally, so a CPU slot's ring R / press rings / G only ever hold the real P2 port byte (0 unless a human drives P2).
- LIVE (idle window, no scripted input): P1 mancom=1, P2 mancom=0 (0x54fc00/0x54fc58) in f2700-5500; P2 moveid (0x54fc58+0x2a) changed 0 -> 13 -> 193 -> 177 -> 1 ... (autonomous), while 0x54fccd, 0x54fcce and BOTH rings (0x563f90 and 0x564010, 128 B each, sampled every 100 frames = full coverage) stayed 0 in all 29 samples. So the CPU produces moves without any input bits.
- CPU path writes MOVE IDS, not bits: ai_RunStateMachine 2a890 -> ai_StatePickAttackMove 2ab2c / ai_StartMoveScript -> stores fighter+0x2c (stob ...0x2c( at 2ab24, 2b33c..2b8a0, 2bb2c..2e314) and the picked id goes into ring 0x564290 (26544 from 0x5645d6[p], 27a30 from 0x5645be) and 0x564390 (+0x2a history). Rings R (0x563f90), 0x564090 and G (0x564190) are written only at 25ef8/25f1c/25f40/25f98 (from the real port bytes) and cleared at 26fcc..2705c; no ai_* store targets them (checked every load of ring pointers 0x564594/98/9c/a0/a4 followed by a store: only 0x5645c8 flags, 0x5645b4 counter, and the 0x564290/0x564390 history edits at 29c88/29da8).
- ai_opcodes.md OPEN 'how a CPU-controlled fighter's input byte is produced' is therefore CLOSED: it is not produced. Human move scripts (IN/DIRM operands, ai_opcodes.md R3) compare the nibble layout above against ring R/G; CPU decisions bypass them.
- Not proven: whether hardware ever sets bit3 (no consumer, not drivable in the harness).
