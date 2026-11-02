# DOA arcade DATAMAP (11-02)

Proof levels: PROVEN = debug string / float op / direct xref meaning; OPEN = unproven. Nothing guessed is marked DONE.

## Fighter record (base 0x54fc00 P1, 0x54fc58 P2, stride 0x58)

| off | type | name | proof |
|---|---|---|---|
| +0x0 | u8 | mancom | debug str 0x4d00 test_PrintPlayerDebug@0x5100 |
| +0x1 | u8 | chrnum | debug str |
| +0x2 | u8 | chrcol | debug str |
| +0x4 | f32 | pos_x | debug str + movr |
| +0x8 | f32 | pos_y | debug str + movr; OPEN: round_CheckKO@float cmp <=0 on +8 (health? conflict) |
| +0xc | f32 | pos_z | debug str + movr |
| +0x14 | s16.16 | drct (facing) | debug str, /65536*360 |
| +0x18 | s16.16 | atkdrct | debug str |
| +0x1c | s16.16 | bodydrct | debug str |
| +0x28 | u16 | anime (anim id) | debug str |
| +0x2a | u8 | move/state id | xref names; round_CheckKO tests 0x34..0x3f = KO range (partial) |
| +0x2b | u8 | actcodeflg | debug str |
| +0x30 | u8 | updownhead | debug str |
| +0x32 | u8 | attackpoint | debug str |
| +0x33 | u8 | attacksta | debug str |
| +0x34 | u8 | animeflip | debug str |
| +0x35 | u8 | animeflg | debug str |
| +0x37 | u8 | hitattack (hit flag) | debug str |
| +0x38 | u8 | hitbody | debug str |
| +0x39 | u8 | hitstage | debug str |
| +0x3e | u8 | beatsta | debug str |
| +0x3f | u8 | skysta | debug str |
| +0x40 | u8 | downhit | debug str |
| +0x41 | u8 | actcancel | debug str |
| +0x42 | u8 | graspsta | debug str |
| +0x43 | u8 | dwnasta | debug str |
| +0x44 | u8 | mountsta | debug str |
| +0x46 | u8 | atkheight | debug str |
| +0x47 | u8 | ringhit | debug str |
| +0x4a | u8 | drctajstflg | debug str |
| +0x4b | u8 | damagenum | debug str |
| +0x4d | u8 | hitgrasp | debug str |
| +0x55 | u8 | a.c.use | debug str |

OPEN fields (no proof): health value (+0x08 float candidate, conflicts with pos_y), guard flag, anim frame counter, all gaps between listed offsets.

## Round / mode bytes

| addr | meaning | proof |
|---|---|---|
| 0x54fd13 | round winner (1=P1,2=P2) | round_CheckKO writes |
| 0x54fcfc | round state, 6 = KO/round over | round_CheckKO writes |
| 0x5555e3 | round-over flag | round_CheckKO writes |
| 0x54fcb3 | mode byte (==2 suppresses KO sound) | round_CheckKO read; OPEN: full enum |
| 0x5555ac / 0x5555b8 | camera mode / camera struct | cam_UpdateByMode 0x7d420; OPEN: field layout, renderer read (TGP 0x880080) |

OPEN: true stage id byte, character/costume/stage select bytes, hit/hurt volume tables, ai_ScriptInterpreter 0x28910 opcodes, move table 0x95750 decode.

## Jump tables (78): see ghidra/jtab.tsv (bx addr, table addr, count, status, targets). Proof: ld T[idx*4]; bx.

## Globals (RAM operands, 1877): ghidra/ramtab.tsv

Columns: addr, width-set, ..., xref count, top accessor functions. All typed by access width only; names for fighter/round/camera above; the rest are UNNAMED = OPEN.

Total RAM operand addresses: 1877. Named/proven: ~45 fighter+round fields. Unmapped (unnamed): 1832.
