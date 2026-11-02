import re
rows=[l.rstrip('\n').split('\t') for l in open('ramtab.tsv')]
out=["# DOA arcade DATAMAP (11-02)\n",
"Proof levels: PROVEN = debug string / float op / direct xref meaning; OPEN = unproven. Nothing guessed is marked DONE.\n",
"## Fighter record (base 0x54fc00 P1, 0x54fc58 P2, stride 0x58)\n",
"| off | type | name | proof |","|---|---|---|---|"]
F=[("0","u8","mancom","debug str 0x4d00 test_PrintPlayerDebug@0x5100"),("1","u8","chrnum","debug str"),("2","u8","chrcol","debug str"),
("4","f32","pos_x","debug str + movr"),("8","f32","pos_y (height, 1.0 at floor)","debug str; GOOBI_STAND.md RAM dumps (1.0 on floor); round_CheckKO Y<=0 = fell out of ring (RESOLVED: not health)"),("c","f32","pos_z","debug str + movr"),
("14","s16.16","drct (facing)","debug str, /65536*360"),("18","s16.16","atkdrct","debug str"),("1c","s16.16","bodydrct","debug str"),
("28","u16","anime (anim id)","debug str"),("2a","u8","move/state id","xref names; round_CheckKO tests 0x34..0x3f = KO range (partial)"),("2b","u8","actcodeflg","debug str"),
("30","u8","updownhead","debug str"),("32","u8","attackpoint","debug str"),("33","u8","attacksta","debug str"),("34","u8","animeflip","debug str"),("35","u8","animeflg","debug str"),
("37","u8","hitattack (hit flag)","debug str"),("38","u8","hitbody","debug str"),("39","u8","hitstage","debug str"),("3e","u8","beatsta","debug str"),("3f","u8","skysta","debug str"),
("40","u8","downhit","debug str"),("41","u8","actcancel","debug str"),("42","u8","graspsta","debug str"),("43","u8","dwnasta","debug str"),("44","u8","mountsta","debug str"),
("46","u8","atkheight","debug str"),("47","u8","ringhit","debug str"),("4a","u8","drctajstflg","debug str"),("4b","u8","damagenum","debug str"),("4d","u8","hitgrasp","debug str"),("55","u8","a.c.use","debug str")]
for o,t,n,p in F: out.append(f"| +0x{o} | {t} | {n} | {p} |")
out+=["\nOPEN fields: health (NOT in the 0x58 record: no 16/32-bit life field; +0x10 float init 1.0 is OPEN, likely scale), guard flag, anim frame counter (per-fighter script state lives in a second array at 0x56ac14..0x56ac80, see below), unlisted offsets 0x3 0x10 0x20 0x22 0x24 0x26 0x2c-0x2f 0x31 0x36 0x3a-0x3d 0x45 0x48-0x54 are accessed (ramtab) but unnamed = OPEN.

Ghidra: block WORKRAM 0x500000-0x5fffff (uninit) and struct Fighter (0x58) applied at g_fighter1/g_fighter2 (scripts/SetupRam.java).\n",
"## Round / mode bytes\n","| addr | meaning | proof |","|---|---|---|",
"| 0x54fd13 | round winner (1=P1,2=P2) | round_CheckKO writes |",
"| 0x54fcfc | round state, 6 = KO/round over | round_CheckKO writes |",
"| 0x5555e3 | round-over flag | round_CheckKO writes |",
"| 0x54fcb3 | game mode byte, values 0..4 seen (==2 suppresses KO sound, 1 = credit mode in game_HandleStartInput) | round_CheckKO, game_HandleStartInput; OPEN: enum names |",
"| 0x54fcb4 | play-mode byte, values 0,2,3 compared with 0x54fcb3 | game_HandleStartInput; OPEN: enum names |",
"| 0x5555ac / 0x5555b8 | camera mode / camera struct | cam_UpdateByMode 0x7d420; OPEN: field layout, renderer read (TGP 0x880080) |",
"\nOPEN: true stage id byte, character/costume/stage select bytes, hit/hurt volume tables, ai_ScriptInterpreter 0x28910 opcodes, move table 0x95750 decode.\n",
"## Jump tables (78): see ghidra/jtab.tsv (bx addr, table addr, count, status, targets). Proof: ld T[idx*4]; bx.\n",
"## Globals (RAM operands, 1877): ghidra/ramtab.tsv\n","Columns: addr, width-set, ..., xref count, top accessor functions. All typed by access width only; names for fighter/round/camera above; the rest are UNNAMED = OPEN.\n"]
n=len(rows)
out.append(f"Total RAM operand addresses: {n}. Named/proven: ~120 (fighter, volumes, round, ring). Unmapped (unnamed): {n-120}.\n")
open('DATAMAP.md','w').write("\n".join(out))
