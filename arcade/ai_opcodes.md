# DOA arcade: move-input script VM (0x28910) + move table (0x95750)

Name note: `ai_ScriptInterpret` is NOT an enemy-AI VM. It is the per-frame move-command recognizer: it matches input-history rings against per-character scripts. A script ending `RESULT id` yields a move id later passed to `fighter_StartMove(id)` (decomp ~18317 `fighter_StartMove(field_0x2c, player)`; fighter_StartMove @22822 sets `moveid`, `+0x2c=0xff`, `+0x2d = table[chr][moveid*8+3]`). So table index = moveid (proven).

## OPEN (unproven, not guessed)
1. Direction/button bit names. Operand high-nibble bits 0x10/0x20/0x40/0x80; 0x40/0x80 swap when mirror flag 0x5645e6[player]==1 (left/right-type). Low-nibble bits 1/2/4/8 not mapped to P/K/H/F. So NO P/K notation given; move_table.tsv shows raw operand hex.
2. Pair table 0x956f0 (2 B x 48): meaning of each pair (entry +2). Only access code proven (move_GetNextMove 0x24400, move_GetEntryFlagByState 0x25b20).
3. Entry count of table 0x98db0 (chr 12): 212 is an upper bound (next block 0x99450). Other counts = pointer gaps (tables contiguous); only code bound: class-6 stop in hit_BuildHitBuffers 0x25940 (idx>=0x9b).
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
Tables: 0x95790 chr 0,3,7,9,10,13,14 (200 entries; chr 7 uses script base 0xa4520, others 0xa3080); 0x95dd0 chr 1 (238); 0x96540 chr 2 (214); 0x96bf0 chr 4 (204); 0x97250 chr 5 (214); 0x97900 chr 6 (194); 0x97f10 chr 8 (228); 0x98630 chr 11 (240); 0x98db0 chr 12 (<=212, OPEN 3). 1944 rows total.
Script bases 0xa7680[chr]: 0xa3080 (0,3,9,10,13,14), 0xa3bb0 (1), 0xa4520 (2,7), 0xa4ca0 (4), 0xa55b0 (5), 0xa5c20 (6), 0xa6490 (8), 0xa6ed0 (11), 0xa7630 (12).

| off | type | field | proof |
|---|---|---|---|
| +0 | u16 | anim / motion id | move_GetEntryWord0 25800 -> fighter.anime (+0x28) in fighter_UpdateAnimIndex; hit_BuildHitBuffers passes it to motion_RunMoveScript |
| +2 | u8 | pair-table index (0x956f0) | move_GetNextMove 24400 (returns tbl[2i], moveid = tbl[2i+1]); move_GetEntryFlagByState 25b20. Meaning OPEN 2 |
| +3 | u8 | state class -> fighter +0x2d | fighter_StartMove 22822; move_GetStateClassFor 24360 |
| +4 | u8 | hit-data index, 0xff none | class 5: 0x9c630[chr] stride 0xc (atkheight +0xb); class 2/3: 0x9d8c0[chr] stride 0x14 (+0xa hitgrasp, +0xb atkheight, +0xd priority, +0x12 dmg scale): fighter_StartMove, move_CompareMovePriority |
| +5 | u8 | knockback/reaction id | hit_LoadKnockbackParams 303d0 -> 0x5647d2[player] -> float table 0xb5f30 |
| +6 | u8 | same, used when other fighter is in class 0xc, or +0x2e==1 and class not 2/3 | hit_LoadKnockbackParams |
| +7 | u8 | pushback strength index -> float table 0xb5ff0 | hit_SetPushbackVelocity 32210 |

Classes 7,8,9,0xf use a separate 16-byte table (id 0x30..0xb7 -> 0x9bdb0+(id-0x30)*0x10; else *(0x99450+chr*4)+id*0x10, id+=0x78 if >0xb7): out of scope, not dumped.

## move_table.tsv
Columns: table, chars, moveid (decimal), raw8, anim_u16, pair_idx, class, hit_idx, kb5, kb6, push7 (hex), scripts.
`scripts` = every decoded script whose RESULT == moveid: `b<base>@<addr>:` from that char set's script base, `D@<addr>:` from the default fallback list 0xa2910. Tokens in execution order = newest input first (history scanned backwards); operands raw hex (OPEN 1). Empty = no decoded script yields that id (reached via pair-table chains or scripts excluded by OPEN 8; link not proven).
