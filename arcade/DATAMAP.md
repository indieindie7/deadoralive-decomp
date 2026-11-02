# DOA arcade DATAMAP (11-02)

Proof levels: PROVEN = debug string / float op / direct xref meaning; OPEN = unproven. Nothing guessed is marked DONE.

## Fighter record (base 0x54fc00 P1, 0x54fc58 P2, stride 0x58)

| off | type | name | proof |
|---|---|---|---|
| +0x0 | u8 | mancom | debug str 0x4d00 test_PrintPlayerDebug@0x5100 |
| +0x1 | u8 | chrnum | debug str |
| +0x2 | u8 | chrcol | debug str |
| +0x4 | f32 | pos_x | debug str + movr |
| +0x8 | f32 | pos_y (height, 1.0 at floor) | debug str; GOOBI_STAND.md RAM dumps (1.0 on floor); round_CheckKO Y<=0 = fell out of ring (RESOLVED: not health) |
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

OPEN fields: health (NOT in the 0x58 record: no 16/32-bit life field; +0x10 float init 1.0 OPEN, likely scale), guard flag, anim frame counter (per-fighter script state in a second array at 0x56ac14..0x56ac80), unlisted offsets 0x3 0x10 0x20 0x22 0x24 0x26 0x2c-0x2f 0x31 0x36 0x3a-0x3d 0x45 0x48-0x54 are accessed (ramtab) but unnamed = OPEN.

Ghidra: block WORKRAM 0x500000-0x5fffff (uninit) and struct Fighter (0x58) applied at g_fighter1/g_fighter2 (scripts/SetupRam.java).

## Round / mode bytes

| addr | meaning | proof |
|---|---|---|
| 0x54fd13 | round winner (1=P1,2=P2) | round_CheckKO writes |
| 0x54fcfc | round state, 6 = KO/round over | round_CheckKO writes |
| 0x5555e3 | round-over flag | round_CheckKO writes |
| 0x54fcb3 | game mode byte, values 0..4 seen (==2 suppresses KO sound, 1 = credit mode in game_HandleStartInput) | round_CheckKO, game_HandleStartInput; OPEN: enum names |
| 0x54fcb4 | play-mode byte, values 0,2,3 compared with 0x54fcb3 | game_HandleStartInput; OPEN: enum names |
| 0x5555ac / 0x5555b8 | camera mode / camera struct | cam_UpdateByMode 0x7d420; OPEN: field layout, renderer read (TGP 0x880080) |

OPEN: true stage id byte, character/costume/stage select bytes, hit/hurt volume tables, ai_ScriptInterpreter 0x28910 opcodes, move table 0x95750 decode.

## Jump tables (78): see ghidra/jtab.tsv (bx addr, table addr, count, status, targets). Proof: ld T[idx*4]; bx.

## Globals (RAM operands, 1877): ghidra/ramtab.tsv

Columns: addr, width-set, ..., xref count, top accessor functions. All typed by access width only; names for fighter/round/camera above; the rest are UNNAMED = OPEN.

Total RAM operand addresses: 1877. Named/proven: ~120 (fighter, volumes, round, ring). Unmapped (unnamed): 1757.

## Hit / hurt volumes (PROVEN: decomp of hit_LoadAttackTable / hit_LoadHitboxTable + RAM dumps in pcport GOOBI_STAND.md)
| addr | meaning |
|---|---|
| 0x554c30 + p*0x3c + part*4 | body-part slot: byte0 type (1 sphere, 3 capsule), byte1 table index |
| 0xc1090 + chr*0x28 + idx*4 | ROM ptr table -> sphere record float[5]; [3]=radius PROVEN, [1][2] offsets OPEN |
| 0xc05f0 + chr*0x78 + idx*4 | ROM ptr table -> capsule record float[7]; [6]=radius PROVEN, [1..5] endpoints OPEN |
| 0x5503c0 + p*0xb4 + i*0xc | body sphere world pos (3 floats), 15 parts; radius 0x550530 + p*0x3c + i*4 |
| 0x552610 + p*0x168 + i*0x18 | body capsule pos (6 floats); radius 0x5528e0 + p*0x3c + i*4 |
| 0x554bb0 + p*0x3c + part*4 | attack-volume slot (byte0 ==1 active, byte1 index); ROM ptrs 0xbf580 + chr*0x78 + idx*4, record radius [3] |
| 0x552960 + p*0xb4 + i*0xc | attack sphere world pos, 15 parts; radius 0x552ad0 + p*0x3c + i*4 |
| 0x9cbe0 + chr*4 | ROM ptr -> move hit entries, 0x14 B each (byte3 ==1 hit active, byte 0x10 != 0xff); index from move_GetCurrentHitIndex |
| 0x56ac14..0x56ac80 | per-fighter script/anim state (motion_RunMoveScript, round_UpdateFighterTimers): fields OPEN |
| 0x54fd7c / 0x54fd80 | ring half extent X/Z = 24.0f, set in backup_ApplyGameSettings |
| 0x54fd08 / 0x54fd0c | 10.0f, meaning OPEN; 0x54fd77=0x3c 0x54fd78=0x1e round timer params OPEN |

OPEN: true stage id byte (work[0x7251] is only a selector), select bytes, ai_ScriptInterpreter 0x28910 opcodes, move table 0x95750, camera layout, health/guard/anim frame, 4 reachable fallthrough rets (0x8b4c 0x8bbc 0x7a934 0x71e0c) outside Ghidra bodies, ~1757 unnamed globals.
