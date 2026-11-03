# DOA arcade: move-input script VM (0x28910) + move table (0x95750)

Name note: `ai_ScriptInterpret` is NOT an enemy-AI VM. It is the per-frame move-command recognizer: it matches input-history rings against per-character scripts. A script ending `RESULT id` yields a move id later passed to `fighter_StartMove(id)` (decomp ~18317 `fighter_StartMove(field_0x2c, player)`; fighter_StartMove @22822 sets `moveid`, `+0x2c=0xff`, `+0x2d = table[chr][moveid*8+3]`). So table index = moveid (proven).

## OPEN (unproven, not guessed)
1. [RESOLVED R3] Direction/button bit names. Operand high-nibble bits 0x10/0x20/0x40/0x80; 0x40/0x80 swap when mirror flag 0x5645e6[player]==1 (left/right-type). Low-nibble bits 1/2/4/8 not mapped to P/K/H/F. So NO P/K notation given; move_table.tsv shows raw operand hex.
2. [RESOLVED R1] Pair table 0x956f0 (2 B x 48): meaning of each pair (entry +2). Only access code proven (move_GetNextMove 0x24400, move_GetEntryFlagByState 0x25b20).
3. [RESOLVED R2 (slot count 212)] Entry count of table 0x98db0 (chr 12): 212 is an upper bound (next block 0x99450). Other counts = pointer gaps (tables contiguous); only code bound: class-6 stop in hit_BuildHitBuffers 0x25940 (idx>=0x9b).
4. hit_GetMoveParamA/B, hit_GetDamageScale read entry-4 relative offsets; base unexplained.
5. Selection from candidate list (0x564610+player*4, max 4) to fighter+0x2c not traced; only +0x2c -> fighter_StartMove proven.
6. Tokens 0x17-0x1f, 0x2d-0x2f, 0x33-0xfff8: no handler (nothing consumed). 0x32 ANGLE modes only partly read.
7. Script slot (param_1) meaning: slot arrays are overlapping windows of one pointer array (slot0 @0xa2f20, slot1 @0xa2f30 = same entries shifted by 4); slot -> game situation not mapped.
8. 173 of 783 scanned script pointers did not decode as valid streams (array overrun / non-script data); excluded from move_table.tsv.
9. Opcode 0x23 COND dispatch stub address not separately listed; body is move_CanUseMove 0x2a040.

## Dispatch
Tokens are u16, stored high-to-low: read at ptr, ptr -= 2 (args likewise). Dispatch = compare tree (prog.dis 0x28994..0x28bac), no jump table (jtab.tsv has no entry). Entry: ai_ScriptDispatch 0x287b0, `_2` 0x28810 (opponent ptr).
Setup: `list = *(0xa7680 + chrnum*4)`; `alts = *(list + slot*4)` = array of script ptrs (0 = skip); if no result (be==0xff) retry with default list `*(0xa2910 + slot*4)`.
Loop: cbc(0x5645bc)=1 -> next alternate; cbd(0x5645bd)=1 -> accept. Result be(0x5645be) appended to 0x564610+player*4 (max 4; count 0x564618+player) unless already present or == fighter+0x2c.

State: 0x5645a8 read ptr; 0x5645b4 u16 counter; 0x5645b6/b7 self/other player; 0x5645b8 first-match flag; 0x5645ba last operand; 0x5645c0/c4 own/opp fighter ptr; 0x564590 saved start; 0x564593 history cursor (mod 0x80).
Rings (0x80 B/player, + player*0x80): 0x563f90 raw input 0x54fccd (ptr 0x564594, "R"); 0x564090 from 0x54fcd5 (ptr 0x564598); 0x564190 merged (ptr 0x56459c, "G"); 0x564290 button history (ptr 0x5645a0); 0x564390 own moveid +0x2a history (ptr 0x5645a4); 0x564490 misc (ops 0x25/0x2a). Written each frame at 0x25ef8..0x26544.
Input operand a: bit8 set -> mask 0xff, else mask 0x0f if 0<a<=0xf else 0xf0; compare (mask & ring byte) == (a & 0xff). Bit9 set -> ring R, else G. Most matchers step cursor back once more if a==0 or a>0xf.

## Opcode table (arg words popped; verified in disasm tree AND decomp 25599-26700)
| val | mnemonic | args | effect | handler |
|---|---|---|---|---|
| 0x0000 | CNT | 1 | 0x5645b4 = arg (scan window; underflow -> cbc) | 28db0 |
| 0x0001 | SKIP | 1 | cursor -= arg & 0x7f | 28de0 |
| 0x0002 | SKIPE | 1 | scan arg entries of ring 0x5645a4; any != 0xff -> cbc | 28e20 |
| 0x0010 | IN | 1 | scan back until masked ring byte == arg | 28ea0 |
| 0x0011 | DIRB | 1 | match using OR of 0x564598 history (helper cmd_OrHistoryBytes 291e0) | 29080 |
| 0x0012 | HOLD | 2 | dir arg0 held arg1 frames | 29250 |
| 0x0013 | DIRM | 1 | like IN, fails if mask hit before match | 294a0 |
| 0x0014 | PAIR | 2 | two-direction sequence, ring per arg | 29660 |
| 0x0015 | WIN | 1 | 2-frame OR window on ring 0x564598 | 298e0 |
| 0x0016 | FACE | 0 | fail unless 0x54fcd4 bit4 (P0) / bit5 (P1) set | 29b20 |
| 0x0020 | BTNA! | 1 | compare 0x5645dc[player]; scan ring 0x5645a0; mark found 0xff (consume) | 29b70 |
| 0x0021 | BTNB! | 1 | compare 0x5645da[player]; scan ring 0x5645a4; mark 0xff | 29c90 |
| 0x0022 | BTNOPP | 1 | compare 0x5645da[other]; scan 0x564390+other*0x80 | 29ee0 |
| 0x0023 | COND | 1 | move id; move_CanUseMove (cond table 0xa76c0, 8 B/id); cbc = !usable; always fails if 0x5645e2==1 | body 2a040 |
| 0x0024 | FLAGE4 | 0 | fail if 0x5645e4[player]==0 | 2a330 |
| 0x0025 | BUF1 | 0 | scan ring 0x564490 until entry==1 | 2a360 |
| 0x0026 | OPP43 | 0 | fail if opponent +0x43 (dwnasta)==0 | 2a590 |
| 0x0027 | OPPST | 1 | fail unless opponent +0x2d == arg | 2a550 |
| 0x0028 | BTNA | 1 | as 0x20 without consuming | 29db0 |
| 0x0029 | SELFMV | 1 | fail unless own +0x2a == arg | 29ea0 |
| 0x002a | BUF0 | 0 | scan ring 0x564490 until entry==0 | 2a410 |
| 0x002b | SLOTEMPTY | 0 | fail unless own +0x35==2 and +0x2c==0xff | 2a4c0 |
| 0x002c | FRAMES | 2 | fail unless lo <= 0x5645cc[player] <= hi (u16; popped lo then hi) | 2a4f0 |
| 0x0030 | RSTHIST | 0 | cursor = 0x564590 | 2a5b0 |
| 0x0031 | CLRPTR | 0 | 0x5645b8 = 0 | 2a5d0 |
| 0x0032 | ANGLE | 1 | facing-angle test; modes 0,1,2 write own +0x4c (mode 2 uses TGP) | 2a5e0 |
| 0xfff9 | G561B | 0 | 0x55561b=1; cbc=1 | 2a800 |
| 0xfffa | F50 | 0 | own +0x50=1; cbc=1 | 2a7e0 |
| 0xfffb | F4E | 0 | own +0x4e=1; cbc=1 | 2a7c0 |
| 0xfffc | PRINT | 3 | tile_SetCursor(a,b) + str_FormatCore (debug text) | 2a820 |
| 0xfffd | B3C | 1 | own +0x3c = arg (arg not consumed); cbc=1 | 2a780 |
| 0xfffe | ABORT | 0 | cbc=1 | 2a7b0 |
| 0xffff | RESULT | 1 | cbd=1, be = arg = move id | 2a750 |

Non-opcode helpers: ai_OpDecrementLoop 28ce0, ai_OpSwapInputBits 28d50 (mirror swap of 0x40/0x80).
Evidence for every row: compare-tree targets prog.dis 28994..28bac + handler body. Decode check: 610 scripts end `RESULT id` with consistent arg counts (e.g. @a2d86 `IN(1) RESULT 67`).

## Move table 0x95750
`u32[16]` indexed by fighter.chrnum (+1), chars 0..14 ([15]=0). If actcodeflg(+0x2b)==1 the OPPONENT's chrnum picks the table (fighter_StartMove 22822). Index = moveid. Entry = 8 bytes.
Tables: 0x95790 chr 0,3,7,9,10,13,14 (200 entries; chr 7 uses script base 0xa4520, others 0xa3080); 0x95dd0 chr 1 (238); 0x96540 chr 2 (214); 0x96bf0 chr 4 (204); 0x97250 chr 5 (214); 0x97900 chr 6 (194); 0x97f10 chr 8 (228); 0x98630 chr 11 (240); 0x98db0 chr 12 (212, R2). 1944 rows total.
Script bases 0xa7680[chr]: 0xa3080 (0,3,9,10,13,14), 0xa3bb0 (1), 0xa4520 (2,7), 0xa4ca0 (4), 0xa55b0 (5), 0xa5c20 (6), 0xa6490 (8), 0xa6ed0 (11), 0xa7630 (12).

| off | type | field | proof |
|---|---|---|---|
| +0 | u16 | anim / motion id | move_GetEntryWord0 25800 -> fighter.anime (+0x28) in fighter_UpdateAnimIndex; hit_BuildHitBuffers passes it to motion_RunMoveScript |
| +2 | u8 | pair-table index (0x956f0) | move_GetNextMove 24400 (returns tbl[2i], moveid = tbl[2i+1]); move_GetEntryFlagByState 25b20. Meaning: see Resolved R1 (flag, next moveid) |
| +3 | u8 | state class -> fighter +0x2d | fighter_StartMove 22822; move_GetStateClassFor 24360 |
| +4 | u8 | hit-data index, 0xff none | class 5: 0x9c630[chr] stride 0xc (atkheight +0xb); class 2/3: 0x9d8c0[chr] stride 0x14 (+0xa hitgrasp, +0xb atkheight, +0xd priority, +0x12 dmg scale): fighter_StartMove, move_CompareMovePriority |
| +5 | u8 | knockback/reaction id | hit_LoadKnockbackParams 303d0 -> 0x5647d2[player] -> float table 0xb5f30 |
| +6 | u8 | same, used when other fighter is in class 0xc, or +0x2e==1 and class not 2/3 | hit_LoadKnockbackParams |
| +7 | u8 | pushback strength index -> float table 0xb5ff0 | hit_SetPushbackVelocity 32210 |

Classes 7,8,9,0xf use a separate 16-byte table (id 0x30..0xb7 -> 0x9bdb0+(id-0x30)*0x10; else *(0x99450+chr*4)+id*0x10, id+=0x78 if >0xb7): out of scope, not dumped.

## move_table.tsv
Columns: table, chars, moveid (decimal), raw8, anim_u16, pair_idx, class, hit_idx, kb5, kb6, push7 (hex), scripts.
`scripts` = every decoded script whose RESULT == moveid: `b<base>@<addr>:` from that char set's script base, `D@<addr>:` from the default fallback list 0xa2910. Tokens in execution order = newest input first (history scanned backwards); operands raw hex (OPEN 1). Empty = no decoded script yields that id (reached via pair-table chains or scripts excluded by OPEN 8; link not proven).


## Resolved (11-02)

### R1. Pair table 0x956f0 = "next move after animation end" table (OPEN 2 closed)
Layout: 48 pairs x 2 B = 0x60 B, 0x956f0..0x9574f (next object = move-table pointer array 0x95750). Pair i = `{flag u8 @0x956f0+2i, next_moveid u8 @0x956f1+2i}`. Index i = byte +2 of a move entry: of the 8-byte per-char entries (0x95750 tables) AND of the 16-byte entries (shared 0x9bdb0 table / per-char 0x99450 tables). Proof: move_GetNextMove 24400 (classes 7,8,9,15 read move_GetEntry(...)+2, else 0x95750[chr]+moveid*8+2).
Use (proven): `move_GetNextMove` 24400: `p = entry.+2; fighter.moveid(+0x2a) = pair[p].next; return pair[p].flag`. Callers (decomp): fighter_UpdateStateIdle 20040 / _tail 204e4, UpdateStateStun 20590, UpdateStateDownRecover 21060, fighter_ResumeAfterMove 23da0 (call at 23e08). Runs when the fighter's animeflg==1 (animation finished). flag==0 -> new state class = move_GetStateClass 242a0 (+3 of the 8-byte per-char entry at the new moveid); flag!=0 -> move_GetStateClass_2 24310 (+3 of the 16-byte entry via move_GetEntry 25680). Then fighter +0x2d = class, +0x2c = 0xff.
So flag = which table the NEXT move id lives in (0 = per-char 8-byte table, 1 = 16-byte table 0x9bdb0, ids 0x30..0xb7). Data check: all 27 flag=1 pairs (next ids 62-65, 161-183) have class 9 in the 16-byte table; flag=0 next ids have classes from the char tables only (never 7/8/9/15).
Second reader `move_GetEntryFlagByState` 25b20 (callers 2f6e0, 4b424, 4b590; also inline at 22d94): returns 1 iff pair.flag==0 and next in {0,10} = move ends in neutral idle (0 / 10).
Dump (i: flag,next): 0:0,0  1:0,1  2:0,2  3:0,10  4:0,11  5:0,12  6:0,50  7:0,51  8:1,63  9:1,65  10:1,62  11:1,64  12-23:1,165..176  24-27:1,161..164  28-30:0,23..25  31-32:1,177,178  33-36:0,111..114  37-41:1,179..183  42:0,190  43-47:0,155..159.
Who uses which: pairs 0-5 = self-loops of ids 0,1,2,10,11,12 (idle/walk); 6,7 (->50,51) classes 10-13; 28-30 (->23-25) class 1; 33-36 (->111-114) class 2; 42-47 single-char moves; 8-27,31,32,37-41 referenced only from the 16-byte tables (reaction/knockdown entries). move_table.tsv gained two columns at the end: pair_flag, pair_next_moveid (header pair_idx renamed).

### R2. Per-character entry counts (OPEN 3 closed by layout; one limit stays OPEN)
Pointer array 0x95750: u32 LE [16], index = fighter.chrnum (fighter byte +1; `ld 0x95750[chrnum*4]` at 22d58, 244b4, 25c28); [15]=0. Tables are packed back to back with no gaps, 8 B entries; count = gap/8.
chr -> base (entries): 0,3,7,9,10,13,14 -> 0x95790 (200, shared); 1 -> 0x95dd0 (238); 2 -> 0x96540 (214); 4 -> 0x96bf0 (204); 5 -> 0x97250 (214); 6 -> 0x97900 (194); 8 -> 0x97f10 (228); 11 -> 0x98630 (240); 12 -> 0x98db0 (212: 0x98db0 + 212*8 = 0x99450 exactly, where the u32 pointer array of the 16-byte tables starts, bytes 90940900 50990900 ...). Entry 211 of chr 12 (`6918000e01161602`) has the same shape (class 0x0e, hit 01, kb 16/16, push 02) as the class-14 move at the tail of the other tables; entries 0..211 all have pair idx <48 (max 36) and classes in the common set. Total 200+238+214+204+214+194+228+240+212 = 1944 rows (matches move_table.tsv).
Notes: chr 1 entry 237 and chr 8 entry 227 are all-zero 8 B entries (padding or unused). The class-14 sentinel-shaped entry is NOT always last (chr 1 at 233, chr 2 at 210, chr 8 at 226), so it is a move, not a terminator.
STILL OPEN (blocker): highest moveid each char is actually given. Code never compares moveid to a count (byte index used directly), so counts are slot counts from ROM layout, not a code-enforced limit.

### R3. Controller byte bits (OPEN 1 closed)
Source: test_ScreenInputTest 87d70 prints " ON" (0x87d60) when a bit of `0x54fccd` (player 1; `0x54fcce` player 2, same layout) is set; labels printed by test_DrawInputScreen 883e0 (strings read from prog.bin 0x88230..0x883a0). Row y -> label: 10 UP, 12 DOWN, 14 LEFT, 16 RIGHT, 19 HOLD, 21 PUNCH, 23 KICK, 27 START (counted from the "\n" in each string).
| bit | mask | meaning | proof (test in 87d70) |
|---|---|---|---|
| 0 | 0x01 | HOLD | y19 `& 1` |
| 1 | 0x02 | PUNCH | y21 `>>1 & 1` |
| 2 | 0x04 | KICK | y23 `>>2 & 1` |
| 3 | 0x08 | unknown: not tested by the input screen; no IN/DIRM operand in move_table.tsv has low-nibble bit 8 | OPEN (no test found) |
| 4 | 0x10 | DOWN | y12 `>>4 & 1` |
| 5 | 0x20 | UP | y10 `>>5 & 1` |
| 6 | 0x40 | RIGHT | y16 `>>6 & 1` |
| 7 | 0x80 | LEFT | y14 sign test |
Active-high in RAM: input task (prog.dis 08060..0820c) reads ports 0x1c00002/4/6/8 into bytes 0x54fccc..cf then inverts the dword (081b0 `st` of `not`), so pressed = 1. 0x54fccc = system byte (START1/2 = bits 4/5 per input screen).
Derived: dword 0x54fcd4 = new-press edges (cur & ~prev; P1 byte 0x54fcd5, P2 0x54fcd6); 0x54fcd8 = release edges; 0x54fcd0 = previous-frame copy (0x54fcd1 = P1 previous byte).
Script rings (prog.dis 25ef0..25f98): ring R 0x563f90 = held byte 0x54fccd[p]; ring 0x564090 and ring G 0x564190 = press-edge byte 0x54fcd5[p], and G additionally ORs in the current direction nibble when it differs from the previous frame's (0x54fcd1 & 0xf0).
IN operand a: low nibble = buttons HOLD 1 / PUNCH 2 / KICK 4 (IN(1), IN(2), IN(4) = press edges, the three most common operands); high nibble = DOWN 0x10 / UP 0x20 / RIGHT 0x40 / LEFT 0x80. The mirror swap of 0x40/0x80 therefore swaps RIGHT/LEFT; which one reads as "forward" depends on flag 0x5645e6 and its meaning was not traced. bit8 (0x100) = full-byte mask, bit9 (0x200) = held ring R instead of G. Examples: IN(200) = held stick neutral; IN(310) = held exactly DOWN; IN(250) = held DOWN+RIGHT; IN(290) = held DOWN+LEFT; IN(2a0) = held UP+LEFT.
OPEN (blocker): how a CPU-controlled fighter's input byte is produced. The ring writer only reads 0x54fccd[p]; no separate AI input word was traced.
