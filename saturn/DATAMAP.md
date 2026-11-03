# DOA Saturn data map (00DOA.BIN, load 0x06004000)
Proof levels: P = proven (decomp code read + live peek), C = code only (writers named from decomp xref scan `build/floor/w/rd.py`, `rd.json`), W = writer census only (store watch 0600E6D0:0600E7FF vblanks 7100-9400, `build/floor/w/an.txt`). Nothing here is a guess; C/W rows give the meaning the writer function names/comments imply and are listed OPEN until value-correlated.

## Fighter struct, base 0x0600E6D0 + 0x58*n (n=0 P1, n=1 P2), stride 0x58 (11-02 drill, authoritative)
Evidence key. N = member name from the symbol-name list in 00DOA.BIN @0x6004acd..0x6004c52, declaration order: animespd bodydrct lastdamage damagedisp actcodeflg posestatus downstatus updownhead downdrct attackpoint attacksta animeflip animeflg animereq hitattack hitstage guardsta actcancel graspsta mountsta ringoutsta atkheight plyrdispflg dangerflg drctajstflg damagenum sidespin hitgrasp grplslip beathitsta ukemi_flg dangersetflg comboflg combocnt combostart actcanceluse. A = arcade debug screen test_PrintPlayerDebug (same stride 0x58; offsets in arcade/ghidra/DATAMAP.md). R = reader/writer functions (build/floor/w/rd.json). L = live value set per posture state, from replaying the store watch (build/floor/w/log2.txt vblank 7135-9400, script build/floor/w/rp.py, output phase.json). Posture = +2D: 0 idle, 1 jump, 2 crouch, 3/5/6 attack/move, 9 hit, B/C/D down.

| off | type | name | evidence |
|---|---|---|---|
| +00 | u8 | mancom (active, man or CPU) | A; R 190 fns (game_DecideRoundWinnerAndAdvance 75); peek 01 in fight; zeroed by player_ResetStruct |
| +01 | u8 | chrnum (fighter id) | A; R scene_LoadCharSelectAssets x11; peek 02 for n1 |
| +02 | u8 | chrcol (costume) | A; R scene_LoadCharSelectAssets x5, fight_InitPlayerAnimSlots |
| +03 | u8 | join/side flag 0/1 | R game_UpdatePlayerJoinState x3, game_HandleStartJoin; L 0/1 |
| +04 | s32 16.16 | pos X | A movr; peeks; copy at 0x0600C948 |
| +08 | s32 | pos Y, 1.0 on ground | A; L: +0A/+0B vary only in states 1 and 9 |
| +0C | s32 | pos Z | A; peeks; copy 0x0600C948[2] |
| +10 | s32 | scale/knock height (1.0 on ground) | R fight_UpdateKnockdownStateA/B, game_InitRoundState |
| +14 | s32 16.16 angle | drct (facing) | A /65536*360; L hi half 0/FFFF, frac byte +16 in 209..233 (~295 deg); R fight_AutoTurnToOpponent |
| +18 | s32 16.16 | atkdrct | A; L same value family as +14 |
| +1C | s32 16.16 | bodydrct (cam_UpdateOrbitFighter reads) | N+A; L same family |
| +20 | u16 | HEALTH, starts 0xA0 | peeks A0@7200, 9B@7600, 0 at KO; game_ApplyPendingDamage subtracts +22 |
| +22 | u16 | pending damage | same fn; L +23 in {5,7,10,11,15,30,42} only in posture 9 |
| +24 | s16 | lastdamage (hit amount kept after apply) | N order; L +25 same set persists after posture 9 |
| +26 | u16 | damagedisp (damage display counter) | N order; written in game_ApplyPendingDamage; L +27 0..30 in posture 9 |
| +28 | u16 | anime (animation id; hi byte 0/1/5/0x20/0x21, lo byte +29 many values) | A; L changes only with posture |
| +2A | u8 | move id | R fight_ProcessMoveRequest*, fight_StartThrowReaction; L 42 values (idle 0..10, jump 20-25, attacks 64-215, down 223) |
| +2B | u8 | actcodeflg (1 when hit/down) | N+A; L 1 only in postures 9, B |
| +2C | u8 | posestatus (pose id airborne, 255 otherwise) | N order; L 106,108,215 only in posture 1 |
| +2D | u8 | downstatus / posture (0 idle,1 jump,2 crouch,3,5,6 move,9 hit,0xB-0xD down) | N order; game_CheckRoundWinnerByHealth tests ==0xD |
| +2E | u8 | hit flag (cleared in fighter_ResetMotionState) | R fight_SelectHoldResponse x5, fight_StartWallHitReactionA; L 0/1 |
| +2F | u8 | facing flag (toggles on turn) | R fight_UpdateKnockdownStateB, fight_ProcessMoveRequestHit; L 0/1 |
| +30 | u8 | updownhead | N+A; R fight_ChooseHitReaction, fight_CanBeCounterHeld; constant 0 in the timeline |
| +31 | u8 | downdrct (down direction 0/1) | N order; R fight_PickIntroOrWinMove; L 1 in down postures |
| +32 | u8 | attackpoint (0, 2) | N+A; L 2 only idle/jump/attack |
| +33 | u8 | attacksta (attack phase 0/1/2) | N+A; L nonzero only in postures 2,3,5 |
| +34 | u8 | animeflip (mirror) | N+A; L toggles with +2F |
| +35 | u8 | animeflg (pulse at action boundary, 2 on connect) | N+A; R fight_ProcessMoveRequest*; L 0/1/2 |
| +36 | u8 | animereq | N order; L 1 only in idle |
| +37 | u8 | hitattack (own attack connects) | N+A; R hit_CheckPlayerVsPlayer sets, hit_RunFrameCheck clears; L 1 in attack postures |
| +38 | u8 | hitbody (hit by opponent sphere) | A; R hit_LoopOpponentSpheres; L flickers all postures |
| +39 | u8 | hitstage | A; R fight_UpdateKnockdownStateB; constant in timeline |
| +3A | u8 | guardsta (guard on) | N order; R ai_ScriptSetGuardFromInput, fight_ChooseHitReaction; L 1 in idle/hit while guarding |
| +3B | u8 | hold/step phase 0..3 | P 11-02 (store watch 6600-9400 x2 scripts): 1,2,3 in posture 1 (jump) set by fight_StepFighterPhysics/hit_InitPlayerSlotTables, 0 in idle by fighter_ResetMotionState |
| +3C | u8 | velocity-angle flag 0/2 | P: value 2 in posture 0 set by fight_ProcessMoveRequestIdle, cleared 0 by fighter_ResetMotionState (both players) |
| +3D | u8 | velocity-angle flag 0/1/2 | P for 0/1: 1 in posture 0 by fight_ProcessMoveRequestIdle, cleared by fighter_ResetMotionState / fx_DispatchSlotUpdate; value 2 not seen live (code only) |
| +3E | u8 | beatsta (hit reaction kind 0,2,3,4,8) | A; L only hit/attack/down |
| +3F | u8 | skysta (airborne-hit phase 0,2,3,4) | A; L only posture 9 |
| +40 | u8 | downhit | A; R hit_ClassifyHitHeight; L 1 in down |
| +41 | u8 | actcancel | N+A; R fight_ProcessMoveRequestIdle, KnockdownStateA/B; constant in timeline |
| +42 | u8 | graspsta (grab attempt) | N+A; L 1 only postures 2,3 |
| +43 | u8 | dwnasta | A; L 1 only posture 9 |
| +44 | u8 | mountsta (0,1,3) | N+A; R fight_ChooseHitReaction, fight_ComputeKnockbackVelocity; L 3 in 1/2/9 |
| +45 | u8 | ring clamp flag | R fight_CheckOutOfRing, fight_ClampPlayerToRing |
| +46 | u8 | atkheight (1 high, 2 mid, 3 low) | N+A; L 1..3 in attack postures |
| +47 | u8 | ringhit / wall flag | A; R wall reactions, fight_CheckOutOfRing |
| +48 | u8 | plyrdispflg (draw flag, default 1) | N order; R ai_UpdateCpuMain, game_RunRoundEndSequence |
| +49 | u8 | ring-out landing flag (was 'hit-effect flag') | P 11-02: setter fight_UpdateRingOutPushback @0605dfdc (decomp 31979/32012: +49=1) when a grounded fighter (+44==1, Y==ground) in posture 9/0xF/0xA-0xB is OUTSIDE the ring bounds (inside = goto LAB_0605e2ce skips). Reproduced: poke P1 X=0x7F000000, Y=1.0, posture 9, +44=1, +51=0 held vb 7500-7510 -> 12 nonzero stores by 0605DFDC (build/dm/wc5.log). Readers fx_SpawnHitEffects (also needs +48), fight_ProcessMoveRequestHit, fight_UpdateKnockdownStateB. Cleared by ResetMotionState / ClearPlayerFlags. Scripted play never leaves the ring, so only ring-out sets it |
| +4A | u8 | drctajstflg | P: toggles 0/1 via fighter_ConsumePendingFlags + fighter_ApplyHitResult in postures 0,1,3,5,10,13 |
| +4B | u8 | damagenum (number popup) | P: 1/0 by fight_ApplyHitPushback + hit_InitPlayerSlotTables only in postures 9,10 |
| +4C | u8 | side (+34 = +4C ^ 1) | **P** 11-02. Forced CPU-AI path: env DOA_CALLFN=06064530@7500 (saturnkit hook) calls ai_ScriptSetFacingFlag; pool 0602FA04 -> 0600E728 (P2) so it stores P2 +4C (0600E774) = 01 from DOA:06064530 (VBlank 7500, log build/dm/wc9b.log). Follow: DOA_CALLFN=...,0605B66C@7504:1 (fight_ApplyMoveRequestFacing) with P2 +2A poked: 1F->+34(0600E75C)=01 (=+4C), 2B->01 (=+4C), 1E->00 (=+4C^1), 21->00 (=+4C^1) (logs build/dm/wc10_*.log). Retail reach: only via CPU-AI script opcode/queued choice 1E..21 (gate AI flag +6==1, ai_UpdateScriptState @06064bcc) | |
| +4D | u8 | hitgrasp (4..9) | P: values 4,5,6,7,8,9 live in posture 3 (and 2) written by fight_SetupHoldFromMove |
| +4E | u8 | DEAD (never set) | whole 00DOA.BIN has only zero stores to it (fighter_ResetMotionState 8081, init 5128); no other fn reads it (rd.json); 11000-vblank run: zero only. Padding byte |
| +4F | u8 | hit-react flag | P: 1 in postures 0,2,3,5 set by fx_DispatchSlotUpdate, cleared by fight_ClearPlayerFlags / 0 in 9 (slot-event flag, not only hits) |
| +50 | u8 | counter-hold roll flag | P: setter ai_RollCounterHold @06067610 (decomp 39223: math_RandomThreshold == 1 -> +50=1, gate fighter +44==1 and AI timer cond): seen nonzero once, P2, vb 17594 in the random-input CPU run (build/dm/wc3.log). Cleared by fx_DispatchSlotUpdate, fight_StartThrowPair, fight_StartPairedMoves, fight_ChooseHitReaction; read by fight_ProcessMoveRequestHit @30124, fight_UpdateKnockdownStateB @30345 |
| +51 | u8 | pushback active | P: 1 in postures 9,10, 0 in 12; writer fight_UpdateRingOutPushback @0605dfdc (not fight_ApplyHitPushback) |
| +52 | u8 | slot-event flag (paired with +54) | P: stores identical to +54 (fx_DispatchSlotUpdate sets, fight_ClearPlayerFlags clears, fight_StartThrowPair/StartPairedMoves), postures 3,4,6; NOT a combo flag by writers; readers game_UpdateRoundOutcome, hud_UpdateComboCounters |
| +53 | u8 | hit counter 0..2 | P: 0/1/2 live in posture 3 by fx_DispatchSlotUpdate, fight_StartThrowPair, fight_StartPairedMoves, fighter_ResetMotionState; readers fight_ChooseHitReaction, hud_UpdateComboCounters |
| +54 | u8 | throw/paired flag | P: 1 postures 3,4,6 set by fx_DispatchSlotUpdate, fight_StartThrowPair, fight_StartPairedMoves; cleared by fight_ClearPlayerFlags |
| +55 | u8 | actcanceluse | A a.c.use; R KnockdownStateA/B |
| +56,+57 | | padding | no readers or writers in rd.json |

n2 (0x0600E780) and n3 (0x0600E7D8) are NOT fighters (census build/floor/w/an.txt): n2+0x00 camera spherical offset output (cam_CalcSphericalOffset, 2263 writes); n2+0x0C (0x0600E78C) per-player mode byte; n2+0x3B (0x0600E7BB) round timer byte 0..0x62 (game_TickRoundTimer, 1720 writes); n3 block zeroed by match_InitRoundState; n3+0x18 (0x0600E7F0) round number 0..4 (game_RunRoundEndSequence, game_RunPostRoundPrompt).

## 0x0600D960 = CAMERA MODE (11-02, item 2 CLOSED; was mislabeled "game state")
Consumer: ai_UpdateCpuMain @06070f6x is really the camera-mode dispatcher: switch(*0x0600D960), cases 0..0x13 (case 0x12 = default no-op). cam_UpdateDispatch @06075f18 re-latches on mode change; camscr_OpStop sets it from camera-script byte. Writers: game_RunRoundEndSequence (9,15,7,8), game_RunPostRoundPrompt (5), game_UpdateRoundResultArray (7), menu_ModeSelectInput (7/8), camscr_OpStop (script data), sys_UpdateDebugPadMenu + game_DecideRoundWinnerAndAdvance (queued value, 0xFF = none), mode 5 sets 6, 0x11 sets 0x12, 0x13 sets 0xFF.
Proof: watch 0600D960 over a full run (build/dm/d960/log.txt, same input): vb270 =1 (title) | 7135 =7 | 7317 =0 (script) | 7318 =2 (fight) | 8408 =5 then 6 | 8589 =3 | 8788 =8 | 8850 =2. Forced sweep: poke 0600D960=NN000000@7330-7500, shot 7500, all 20 values (build/dm/cs/sheet.png, cs/N/shot-7500.png, peek confirms value). Each look differs and matches the handler.
| val | name (handler) | look (shot) |
|---|---|---|
| 0 | FollowFixed: cam_CopyFighterPositions + ai_CopyTableBlock + cam_CalcSphericalOffset, follow distance reset unless mode 7/F | standard side view, sunset |
| 1 | FollowFlip: same with cam_CheckAngleThreshold_2 | opposite side, jungle behind |
| 2 | FightMain: cam_LatchFighterPositions + inner switch on gensoku (ai_UpdateStateMachine / orbit 0,1 / follow distance) | standard fight cam (default in rounds) |
| 3 | OverShoulder: ai_ActionExecuteB/C with arena_IsOutOfBounds + fight_GetAngleOffset | single fighter close, jungle |
| 4 | TopDown: ai_UpdateFighterState | overhead, fighters tiny |
| 5 | RoundIntroLow: cam_UpdateCameraState_2 then mode := 6 | low angle, both fighters large |
| 6 | FollowCam: cam_UpdateFollowCamera | wide standard |
| 7 | ResultScriptA: cam_Latch + ai_PickPatternByte picks camera script, cam_RunScript (round end) | wide, sunset |
| 8 | ResultScriptRandom: libc_RandNext/0x17 picks one of 23 scripts (victory) | wide |
| 9,10 | PresetUpdate: cam_SelectPresetUpdate | close, beach left |
| 0xB | ScriptTable[0] + cam_ResetScriptFlags + cam_RunScript | high overview |
| 0xC | SetupFighterFollow(fighter): cam_SetupFighterFollow one-shot | high overview |
| 0xD | FollowFighter(fighter): cam_UpdateFollowCamera_2 | low very close |
| 0xE | ScriptTable[1] | very high overhead |
| 0xF | ScriptByPattern: pose code 0xB picks table entries 0x20/0x24 | floor corridor / blur |
| 0x10 | DollyToFighter: ai_ActionExecuteB + fight_GetAngleOffset | close on one fighter |
| 0x11 | sets 0x12 (hold) | standard |
| 0x12 | no-op (default) | standard |
| 0x13 | CopyPositions + CopyTableBlock, then clears queue 0xFF | standard |

## 0x0602FA40 = CPU AI STYLE index 0..0x1B (11-02, item 4 CLOSED by poke test; NOT a monotonic difficulty)
Layout gotcha: byte FA40 = style, byte FA41 = separate var (default 01; a 32-bit poke with 00 there clobbers it and changes the run, 61 vs 10 P2 move changes). Poke format VV010000.
Readers (all byte reads, pool refs in 00DOA.BIN): ai_UpdateAttackChoice (switch: {2,7,9,0xB,0xF} / 4 / 5 / 0x10 / 0x12 hold / default select different move-table pointers), ai_ScriptSelectReactionLevel (==6, ==7 override reaction), ai_UpdateScriptState (compares 3,4,5,6,7,0xA), ai_DispatchStateHandler, ai_CheckInputCommandStart, ai_CheckRangeForAttack, ai_ResolveScriptParam, game_SelectStateByFighterMode (4,5), fight_ClampPlayerToRing; menu_DrawTitleText prints string table[idx] (menu shows the style name). Writer: menu_ModeSelectInput, +-1 wrap 0x1C.
Poke test: SATURN_RTC=1000000000, same input, poke 0602FA40=VV010000 held vblank 6000-9400, store watch 0600E728:0600E77F (P2 struct, the CPU). Count of P2 move-id (+2A, 0600E752) changes: style 00 -> 76, 02 -> 129, 04 -> 88, 07 -> 129, 0E -> 59, 1B -> 59. Identical counts inside {2,7} and {0E,1B}, matching the switch groups; total stores 31268/32571/32042/32571/28926/28926. Logs build/dm/ai/VV/log.txt, script build/dm/ai.sh. So P2 CPU behaviour is selected by this byte; it is a style/pattern index, 0 is not "easiest".

## Camera
| addr | meaning | proof |
|---|---|---|
| 0x0600C948 | per-player copy of fighter pos (X, Y, Z...) | P: peek = fighter +04/+08/+0C values |
| 0x06019BE0, stride 0x78 | per-player camera angles (s16 at +2, +6 read by camera_SetupPlayerMatrix @06051d74) | P read; peek 00003A94 @7000 -> 0000387A @7600 changes |
| 0x0602A040 / 0x0602B360 / 0x0602B1B0 | camera target / look-at / output angle tables | C (camera_SetupPlayerMatrix pointers) |
| 0x0600D5EC | camera scroll quantity (int, peek 0x180000), used by camera_UpdateFollowFighters @06069644 (>>2 / >>1) | P value; scroll semantics C |
| 0x0600E72C... (struct n1 +4/+5C) | camera_UpdateFollowFighters adjusts 0x0600E6D0+4 and +0x5C (fighter X pair) | C |

## Stage / modes
| addr | meaning | proof |
|---|---|---|
| 0x0600D5E0 | STAGE ID byte; game_CopyStageParams @0606c7e4 indexes table 0x060AE9D8 stride 0x18 (5 words: ptrs 0x0602FDDC..) | P: peek 0B in all fight runs (jungle stage, vblanks 7000-9000); writer fn @0603fb2c (stage picker, see Stage 7 line); id->name map by look below |
| 0x0600D960 | camera mode byte (1 at title/select vblanks 5300-6000, menu_ModeSelectInput sets 7 or 8) | P+C: it is the CAMERA MODE, see section |
| 0x0602FA40 | mode menu cursor (+-1 in menu_ModeSelectInput @060592d8) | C: peek 0 at title |
| 0x060AC0A5 | toggled with ^1 in mode menu (option) | C |
| 0x0600E78C | per-player mode byte; ==5 makes game_ApplyPendingDamage take damage from 0x0602F380 (P1) / 0x0600E5C4->0x0602F382 (P2) | P code; peek 02 |

## Stage id -> look (11-02, P: poke 0x0600D5E0=id held vblank 6300-7400, shot 7400; build/dm/stages.png)
Poke works: scene changes per id. Names are visual descriptions (no name string in table).
0 city highway/overpass, day | 1 temple courtyard, stone stairs | 2 dark hangar, sunset mural | 3 red-gold palace, blue sky | 4 steel tunnel, green floor | 5 steel gate, pale sky | 6 same scene as 1 (palette variant) | 7 TRAINING room (not broken: sparse by design, see Stage 7 line) | 8 rocky canyon night, moon | 9 black void, icy floor | 10 night city street, billboards | 11 sunset beach | 12 desert night, wooden deck, TINA billboard.
Default fight stage 0x0B (sunset beach). 13 valid table entries.

## OPEN (honest)
- Fighter struct CLOSED 11-02 (see Fighter struct table). Rows +3B..+3D, +49..+54 value-correlated 11-02 (store watch 0600E6D0:0600E7FF vblanks 6600-9400 with scripted inputs build/dm/in2.txt + floor/in.txt, analyser build/dm/corr.py, logs build/dm/wc1.log wc2.log): all P; setter pass: +49 P (ring-out, poke), +50 P (ai_RollCounterHold), +4E DEAD (no nonzero writer exists), +4C P (forced ai_ScriptSetFacingFlag @06064530, +34 = +4C ^ 1). +51 writer corrected (fight_UpdateRingOutPushback), +52 renamed (written with +54, not a combo flag). OPEN = 0.
- D960 CLOSED 11-02 (camera mode, 20 values named). 0x0602FA40 CLOSED 11-02 (CPU AI style index, poke test, see section).
- Hidden slot SOLVED (P+C): cursor index 4 (5th portrait, masked dark figure) is skipped by charsel_PadUpdateMoveCursor @0607e6a8 (left: cur==5 -> 4 then -1; right: cur==3 -> 4 then +1) while byte 0x06013B1A == 0. Writer: game_UpdateResultFlags @0603b8a0 sets it to 1 when (u32 at records+0x3c & 0x249249) == 0x249249 (bit 3*k per character k, set on arcade clear, mode<2), i.e. clear arcade with all 8 characters. Proof: poke 06013B18=00000100 from vblank 1 makes the 9th portrait appear in the strip (build/dm/sl/ab.png, stripb.png vs strip.png). Second gate: table 0x060B588C skipped when 0x0600DA20==0 (all 1 at vblank 6000).
- Hi-res RBG ground truth CLOSED 11-02: Mednafen (minimized, build/med/medrec.py, qtrecord of the 400 s attract demo, frames build/med/fr4/m25.png stage 1 and m52.png stage 11) vs ours (build/dm/st/1, st/11 shot-7400, pair build/med/fr4/pair.png + ours.png): same RBG0 floor texture, red-leaf band, swirl pattern, perspective rows; ours matches at texture/projection level (camera distance differs: attract demo camera vs forced fight camera, so pixel-exact overlay not possible). Manual: VDP2 User's Manual ST-058-R2 ch.6 sec 6.3 rotation parameter table, 6.4 coefficient table (mirror infochunk.com/saturn/segahtml_en/hard/vdp2/hon/p06_30..p06_43). BLOCKER: printed page numbers not verifiable (no local PDF; mirror shows none). Keyboard inject into minimized Mednafen not possible (SDL needs focus), so no forced-stage capture.
- Stage 7 CLOSED 11-02 (P+C, no emulator bug): stage 7 = TRAINING room, disc files TRE1/TRE2A/TRE3 (FAD 8194-8238; TRE2A only 32327 B vs 101-128 KB for other stages = sparse by design). Stage id writer: fn @0603fb2c (Ghidra name game_SelectResultVoiceIndex is WRONG, it is the stage picker): if *0x0600D7BC (game mode byte) == 5 -> stage 7, mode 4 -> random from table, mode 1 -> sequential table 0x..fbf4, else table[ (counter)/9 ]; stores to 0x0600D5E0. Mode 5 = training: game_RunFrameLoopMode5 @0603ba80 calls game_ClearPendingDamageBoth every frame (no damage). VDP2 regs 0x3A/0x3C/0x48/0x4A writers (new debug hook DOA_REGW=1 in saturnkit video.cpp logs host fn chain; --watch on shadow 0x060FFCFA..0x060FFD0C gives stores with r4-r7): shadow regs live at gbr(0x060FFC00)+0xC0.. and are DMAed to 0x25F80000 (0x90 bytes) every V-blank by the SGL V-blank-in handler @060A02A6 (no Ghidra function there: gap, name sgl_VBlankInHandler; saves regs, sets gbr, SCU/DMAC ch1 SAR=0x060FFCC0 DAR=0x25F80000 TCR=0x90). Shadow stores: vdp2_SetupLayerD @0606c72c calls vdp2_SetMapOffsetB @0609e8b4(0x25E7D000 x4) -> MPAB N2/N3 = 0x3A3A, MPOFN N2 = 3 (shift 11 = 2x2 chars, 1 word: (3<<6|0x3A)*0x800 = 0x7D000); PLSZ low byte by vdp2_SetFieldFA_bits01/23 @0609e674/e6f0 and vdp2_SetFieldFB_bits45/01 @0609e8a4/eae0 (0x03D0); 0x3C by SetMapOffsetB. Earlier claim 'plane 0x74000 empty' was a hand-calc error: saturnkit vdp2.cpp setup_nbg already gives plane 0x7D000 (CHCTLB 0x131 -> N2 2x2, PNCN2 0x804C 1 word, PLSZ N2 = 1 (2x1 pages, mask 1)), it holds the real name table (page 0x7D000: 82 distinct chars, 943 blank chars 0x0880 -> char 0x3200 = VRAM 0x64000 dither 0/8 pixels; page 0x7D800 solid pal-5 char 0x5BD3). NBG1 CHCTLA=0700 = 512x256 16-col bitmap at 0x40000, empty in training (nothing loads there). Hide test: SATURNKIT_VDP2_HIDE=0x10 removes the green stripes+grey, 0x4/0x8 change nothing (build/dm/h7grid.png). Not proven vs hardware: no Mednafen frame of the training room (no key input to pick Training), but registers, map math and disc data all agree with the game's own computation.
