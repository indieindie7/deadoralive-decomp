# Dead or Alive (Saturn) decomp — NOTES
## Index
1. Source + layout  2. Pipeline  3. Log
## 1. Source + layout
- User 10-27: images on F:\Downloads: Dead-or-Alive_SEGA-Saturn_JA.zip (Japan Rev A, T-3603G V1.002 1997-09-12, 24 tracks), Dead-or-Alive_Arcade_EN.zip (doa.zip, Model 2 roms, epr-19379c/19380c program).
- Unpacked: saturn/image (bin/cue), saturn/cd (354 files, 96.3 MB, via Scorcher/tools/isoextract.py 2352), arcade/doa.zip.
- Main exe 00DOA.BIN 734916 bytes, IP 1st read addr 0x06004000. Per-fighter data XX_DAT.BIN, XXn_TEX/MDL/LAD/TNK.BIN (KS LE TN LU KM KL GY FA RI TR ZA BY ...).
- No public decomp (web 10-26). Never push disc data.
## 2. Pipeline (copied from Astal 10-27)
- ghidra/run.sh <abs log> <args> (project DOA in ghidra/), ghidra/import.sh <file in bin/> <base> = import SH-2 + FindSh2FunctionsMem + CreateAt + ExportFuncInfo + CsDumpAll.
- Then naming slices (Sonnet / Sage), hand_<P>.txt, ApplyNames, export, review, publish indieindie7/deadoralive-decomp.
## 3. Log
- 10-27: import 00DOA.BIN @0x06004000 DONE: 1605 fn (1603 FUN_), decomp_00DOA.c 82929 lines. Round 1: 11 slices ghidra/naming/DOA_1..11.c, prompt ghidra/scripts/prompt_DOA.txt, Sonnet agents write ghidra/naming/q_<n>.txt; then cat -> hand_00DOA.txt, ApplyNames, export.
- 10-27: round 1 Sonnet 11 slices -> hand_00DOA.txt 1603 lines (947 provisional, 1 dup name suffixed); ApplyNames 1603; export F=1605 FUN=0 (funcinfo_00DOA.tsv, decomp_00DOA.c). Next: provisional review via autorun (Sage), srprovapply, publish.
- 10-27: provisional review queued: ckprovctx.py (copied to DeadOrAlive/tools) -> ghidra/review/DOA1-4.txt (947 entries); prompt ghidra/scripts/prompt_r1_doa.txt; Tools/llm/autorun/queue_doa.json (tag doa_, KEEP_ORDER, pid 18460); out Tools/llm/review_doa/doa_<k>_rv.txt. Apply: cat rv -> py -3.13 -I Pandemonium/tools/srprovapply.py ghidra/hand_00DOA.txt <rv>, ApplyNames, export, publish.
- 10-27 ~10:05: first queue_doa crashed (2 autoruns raced on 8090); user killed both; single autorun pid 19856 restarted (resumes from jsonl).
- 10-27 11:28: doa_1 done (237 verdicts); doa_REPORT.md is rewritten per step with RUNNING header, so wait for no queue_doa process. ETA ~15:30.
- 10-27 18:40: doa_1-3 done (237 each, review_doa/doa_<k>_rv.txt); doa_4 skipped (gpu 0 token busy) -> rerun alone queue_doa4.json, tag doa4_, AUTORUN_GPU_ID=1, pid 6676.
- 10-27 evening: review applied (CONFIRM 705, RENAME 191, UNSURE 51), ApplyNames 1603, export F=1605 FUN=0. PUBLISHED github.com/indieindie7/deadoralive-decomp (b88bb21; local tree Documents/github/deadoralive-decomp). Next: round 2 on 51 unsure, other disc code, Model 2 cross-check.
- 10-27: round 2 (Sonnet over review/DOAr21.txt -> rv2_00DOA.txt): 17 confirm, 34 rename, 0 provisional; ApplyNames 1603, F=1605 FUN=0; pushed bc299f4.
- 10-28: other disc code check: only 00DOA.BIN holds SH-2 code (1113 x 0x4f22 prologues; all other 305 .BIN have <5). SDDRVS.TSK = Sega std 68k sound driver (library, skip). OMAKE/ = BMP art. Saturn side DONE.
- 10-28: NEXT = Model 2A arcade cross-check: arcade/doa.zip program epr-19379c.15 (low16) + epr-19380c.16 (high16), ROM_LOAD32_WORD -> arcade/ghidra/prog.bin (1 MB, base 0); data epr-19328.30 + mpr-*. Recipe = MotorRaid/NOTES.md "i960 SLEIGH module" + "Ghidra project MotorRaid2" (lang i960:LE:32:default, ram_code block 0x200000 from boot copy, SetupMotorRaid.java, mrrun.ps1).

## Model 2A arcade (10-28)
- Input arcade/ghidra/prog.bin (1 MB, epr-19379c low16 + epr-19380c high16, i960 LE, base 0). prog.dis = `Documents\Tools\mame\unidasm.exe prog.bin -arch i960 -basepc 0`.
- Boot record: word +0xc = first IP 0x410. 0x410 copies 0x3d0.. to 0xe00000 (until 0xffffffff), copies 0x2c words ROM 0xb0 -> 0x501810, then ret. Real boot at 0x5f0 (flushreg), work-RAM clear 0x500000..0x5fffff at 0x620, checksum 0x520, main loop 0x570.
- NO ROM->fast-RAM 0x200000 code copy (unlike Motor Raid): no store/lda to 0x200000, 1413 call targets all < 0x100000, only 1 call into 0x20xxxx (0x9be70, data). So DOAarc has no ram_code block, prog.bin only.
- Project arcade/ghidra/DOAarc.gpr (i960:LE:32:default, prog.bin at 0). Runner ghidra/doarun.ps1 <log> -process prog.bin -noanalysis -postScript ...; import = ghidra/imp.ps1. Scripts ghidra/scripts: SetupDOA.java (SetupMotorRaid copy, RAM block disabled), ExportFuncInfo.java, CsDumpAll.java (unchanged copies), DeleteTiny.java (new, reads address list). Tools arcade/tools/seeds.py (call targets in ROM, 1273 seeds -> 1272 fns), gaps.py (run from ghidra/, step.sh = export + gaps).
- Gap passes (seeds2.txt = ret-run starts): +813, +375, +314 ... ~11 passes; most late seeds were DATA (ROM has big data tables with 0x0a000000-like words) -> tiny (<=4 byte) junk functions; 2390+337 deleted with DeleteTiny (ghidra/junk*.txt). Stopped when only 8 real new fns per pass.
- Result: 1969 functions, 3930 calls, 0 string refs (strings not defined without analysis; 1287 ASCII runs in prog.bin, 443 `lda 0xADDR` hit a string start, e.g. 0x2820 "TECMO LTD.  DEAD OR ALIVE", 0x2c40 "SOUND INITIALIZE"). All FUN_ (1968, no names yet). 342 of 2167 rets uncovered (mostly data/tails).
- Files: ghidra/funcinfo_doaarc.tsv, ghidra/decomp_doaarc.c (2.9 MB, 1969 fns, 0 decompile failures), seeds.txt, seeds2*.txt.
- 10-28: arcade naming round 1: decomp_doaarc.c cut into 13 slices (~8000 lines) arcade/ghidra/naming/ARC_1..13.c, prompt naming/prompt_ARC.txt (from MotorRaid prompt_r1), 13 Sonnet agents -> naming/q_<n>.txt. Then hand_doaarc.txt, ApplyNames on DOAarc, export, add arcade/ to deadoralive-decomp.

- 10-28 arcade round 1 DONE: 13 Sonnet slices -> arcade/ghidra/hand_doaarc.txt 1968 lines, 179 provisional, ApplyNames 1968, FUN_ 0; gaps.py: 342 uncovered rets (missed functions, next). PUSHED deadoralive-decomp f7bb3e7 (arcade/ dir). Next: arcade provisional review (ckprovctx -> Strata queue), then gap functions.
- 10-28 arcade review DONE: 3 Sonnet reviewers (review/ARC{1,2,3}_rv.txt, prompt review/prompt_r1_arc.txt, tool arcade/tools/provctx_arc.py): 79 confirm 79 rename 21 unsure; applied (backup hand_doaarc.r1.bak), PUSHED 3aa185e. Next: 342 uncovered rets (gaps.py) = missed functions; round 2 on 21 unsure.
- 10-28 arcade review round 2 (review/ARCr2_rv.txt): 15 confirm 5 rename 1 unsure; PUSHED f44e323. Arcade DONE (gap passes exhausted).
- 10-29: Bayman model code = GY (model table 00DOA.BIN 0x397c4 parallel to voice table 0x3fb78). GY1_MDL = SGL PDATA BE, ptrs 0x060bxxxx. Extract for Goobi brawler Stand.

## Model format (10-29)
Tool: C:\goobi\tools\doa_bayman.py (-> C:\goobi\brawler\assets\anim3d\bayman_doa.glb + _atlas.png), render C:\goobi\tools\doa_render.py (blender -b), sheet C:\goobi\marks\bayman_v1.png. Verdict: works, GY1 = Bayman (red beret, red vest, black pants), 21 parts, 1086 tris.
- XY1_MDL.BIN (XY = char code, GY=Bayman), big-endian, load base 0x060b3000 (file[0:4]=0x060bacd8 = file+0x7cd8). Ptr -> file off = ptr-0x060b3000.
- Per part SGL PDATA {pntbl,nbPoint,pltbl,nbPoly,attbl}; points 12 B FIXED16.16 xyz; poly 20 B = normal(3 fx) + 4 u16 idx (tri = repeated idx); ATTR 12 B {flag,sort,texno u16,atrb u16,colno u16,gstb u16,dir u16}. Part blocks laid pts|polys|attrs back to back, parts stored in reverse node order.
- Node table @0x793c, 21 x 44 B: [ptr->PDATA][pos xyz fx][2 words (0; pelvis has 0x8000)][scale 1.0 x3][0,0]. PDATAs @0x7798..0x793b (0x14 each). Pos = offset from parent. Tail @0x7cd8 (26 ptrs/-1) = per-view draw-order lists (unsolved, unused). @0x7d40 7 ptrs = alt pelvis ATTR tables (0x510 apart: texture variants), unused.
- Node idx: 20 pelvis(root), 19 chest, 6 head, L arm 12 upper/11 fore/7-10 hand pieces, R arm 18/17/13-16, L leg 2 thigh/1 shin/0 foot, R leg 5/4/3. Parent chain inferred from offsets (+.455 y = leg link, .275 x = arm link), NOT stored in MDL (likely in GY_DAT/motion; unsolved).
- Limb meshes authored with z = bone axis, no rest rotation in file; tool applies fixed 90deg rx/ry per limb part (ROT in script) for T-pose. SGL y down, forward = -z; glb flips y,z. Units ~metres (height 1.83).
- TEX: hdr 8 B, 7 CLUT16 BGR555 @0x8 (idx0 = 0x7fe0 transparent; pal = colno>>4), dir 8 B entries @0xf0 {w u16,h u16,off u16 (*8 - 0x10000 + 0xe68 = file off), w/8, h}, count = u32 at EOF-8 (431), 4bpp hi-nibble first, pitch w/2, pixels @0xe68. ATTR dir flip: 0x10 H, 0x20 V (looks right). Quad UV = full-texture corners A,B,C,D.
- Unsolved/open: real skeleton + rotations (anim in GY_DAT/LAD?), 8-px wide dir entries 0-8 (possibly 8bpp, used by flat bits, decoded as 4bpp), other costumes (GY2-5 same layout, untested), GY1_OPT/TNK/CMD purpose, exe loader not located (decomp has no named GY loader).

## Animation format (10-29)
GY_DAT.BIN (file off = ptr-0x200000). Motion table @0x2258 (254 slots, 24 valid, see _doa/doalib.motions()). Slot -> 13-ptr list stored at END of its stream data (ptr[12] = list-4).
List idx: 0,1,2 trunk (u32/key: 11+10+11 bit angles, 16-bit units; 2=hips,0=chest,1=head); 3-6 limb quads (5 B = 4x signed 10bit <<6; end-part triple + swivel); 7-10 endpoints s16x3 /4096 (10,8 = feet A,B; 9,7 = hands A,B; A = x<0); 11 root s16x3 (frame0 absolute, rest deltas; y = -hips height, y-down).
Endpoints = stream y-up frame, +1.366 y lifts ankle above ground (ground const from idle min ankle + sole .11). Hips y = -rooty. Reach check: legs <=.91, arms <=.62 OK.
Valid motions (idx:keys): 0:51 8:15 10:15 15:14 16-21:6 26:8 32:8 35:8 36:91 65:11 66:7 67:11 114:4 168:24 188:23 190:19 192:24 195:86 236:26. Script table @0x2650 (6666 op.. ffff) not decoded: no move names. Only m000 = idle (loop, frame50==0).
Tools: C:/goobi/tools/doa_bayman_anim.py (armature, rigid skin, 2-bone IK limbs from endpoints, root bone, 60 keys/s) -> assets/anim3d/bayman_doa_anim.glb; _doa/doalib.py; doa_anim_sheet.py (now draws ground plane)+doa_sheet_stitch.py (blender -b contact sheet). Env DOA_NOTRUNK=1 disables trunk, DOA_NOANCHOR=1 disables pelvis anchor.
Round 2 (10-29): TRUNK SOLVED (default on). Exe pose builder camera_UpdateFighterView @060516d8: M = T*Rz*Ry*Rx per part (draw node @06051f84: RotateC(+0x14 z), RotateA(+0x12 y), RotateB(+0x10 x)); stream word fields 0/1/2 -> X/Y/Z, mirror negates Y,Z. Matches script CFG (a=Y b=X c=Z sg=+1). Brute force of 96 axis/order/sign/transpose combos on chest/head up-vector uprightness over 7 clips: exe order is best (chest 32 deg, head 27 deg mean off vertical). Hips yaw ~63 deg in idle = bladed stance (not error). Hip rotation in idle also pitches 37 deg.
Seated look cause: stream endpoint frame != root frame. Idle feet midpoint is ~0.57 ahead of pelvis xz (root xz 0). Exe computes limb IK in world frame with hip origin from ApplyJointPositions (stack matrix) so exact offset source unresolved. FIX (empirical): pelvis xz = root cumsum + frame-0 feet midpoint xz (per clip). Result v2: idle feet under pelvis, torso upright, stance crouched (pelvis 0.74 above origin, legs bent): probably true DOA stance but still reads low.
Key rate: motion_StepKeyframeInterp @0604a32c: accumulator += FixedMul(step,speed) per game frame, key idx = acc>>16 => 1 key per game frame at speed 1.0. Saturn DOA game loop assumed 60 Hz (not proven in exe) -> FPS=60 (idle loop 0.85 s).
Script table @0x2650 (GY_DAT): 512 u32 ptrs (base 0x200000, file off = ptr-0x200000), 195 unique, to scripts at 0x2e50.. ; record = 6666 [7777] 0000 <motion id u16> 0001 0002 000a <op,arg pairs> ffff. Opcode semantics NOT decoded (motion_ExecuteScriptStep @0604d154 is the lead). Named clips proven: m000 idle only. m036 stands upright with feet alternating small steps (walk/shuffle candidate, unproven); m195 frame ~43 feet y -1.95 (jump/throw? unproven); m195 last frames lie flat (down/getup candidate unproven).
Open: opcode decode for names; pelvis-feet frame offset origin; 30 vs 60 Hz proof; swivel/end-part orientation (hands/feet inherit shin/forearm); knee pole direction.
Round 3 (10-29): ROOT CAUSE FOUND = endpoint streams were swapped. Streams 10,8 = HANDS (y ~1.16-1.26 m, forward z -0.4..-0.7, guard), streams 9,7 = FEET (ankle y const .11 = mesh sole .11 exactly; hand/foot x<0 = A = left). Stream y is y-DOWN like root (world y = -stream y). Feet midpoint z is only -0.075 from pelvis: the "0.57 ahead offset" and pelvis anchor were artifacts of the swap; anchor now opt-in (DOA_ANCHOR=1). Ground = 0 (ankle .11 = sole). Reach check idle: hip->ankle .70/.75 of .91 (knees bent ~80 deg, real data), shoulder->hand .39/.43 of .55 (guard, elbows bent): no scale error. Stance is still a bladed crouch (pelvis .74, hips pitch 37 deg) = data, not tuning; m036 stands upright.
Arms: elbow pole = down + 0.6*back + 0.8*outward (chest x axis, per side; env DOA_ELB). Hands: quad streams idx1 (hand A) and idx3 (hand B) first 3 values = end-part rotation relative to forearm (same trot convention as trunk); fists read forward/up in guard (DOA_NOHAND=1 disables, DOA_HSG=-1 flips). Quad idx0,2 = single-axis (foot pitch, not applied yet). 4th quad value = swivel (hands +48/-49 deg mirrored in idle); likely elbow/knee pole angle, not applied (zero reference unknown).
Script @0x2650 records: only ids 0,65,66,67,114 appear (records 114-116 idle, 81-87 = 65/66/67 punch-like sequence, 158-160 = 114); opcodes still undecoded; motion_ExecuteScriptStep @0604d154 is physics integration, NOT the script decoder (find the real one). No clip names beyond idle. Visual (unproven): m065 hip-kick, m067 kick, m188/m168 punches, m195 jump->down. Sheet C:\goobi\marks\bayman_anims_v3.png. Backups *.bak1029c.

## Arcade model (10-29)
- Script: C:\goobi\tools\doa_arcade_model.py -> assets\anim3d\bayman_arcade.glb (+_atlas.png). Sheet marks\bayman_arcade_v1.png (Saturn above). Work dir C:\goobi\work\doa_arcade. Decoder copy: tools\_doa\m2rom.py, m2dec.py (from MotorRaid).
- Object table: main_data 0x3a170, 16 B/entry (tpa,tha,oba,obc). Bayman ids 10616..10632: chest 10616, head 10617 (273 faces), hip 10618; +x foot/fore/hand/thigh/shin/upper = 10619..10624; -x = 10625..10630; tags 10632; hand poses 10651-10660. Costume blocks repeat at id stride 184.
- Result: 16 parts, 1347 faces, 2360 tris, units metres, coords (x,y,-z). Textured, real 4bpp detail (face, camo, beret band).
- Textures: main_data 0x5c0000 + k*0xc0000, Bayman k=8. 1024x2048 sheet, 16-bit word = 2x2 texel block (bits 12-15 TL, 8-11 TR, 4-7 BL, 0-3 BR). Header: w=32<<(h0&7), h=32<<((h0>>3)&7), x=32*(h2&0x3f), y=32*((h2>>6)&0x1f), cb=(h3>>6)&0x3ff, UV=raw/8; wrap b6/b7, mirror b8/b9; x>=1024 -> x-=1024,y^=1024.
- CAVEAT: textures are grayscale luma only. Real per-character 3D palette / colorxlat NOT found (3D palette 0x1802000 from prog 0x62af0 does not match his colours). Tints manual per (part,cb): head cb8 skin, 11 beret red, 103 hair, 102 band; chest cb102 red vest.
- Skeleton: T-pose uses Saturn node offsets (same metres); arcade skeleton table not located.
- Anim/motion data (offsets only, not decoded): prog.bin move script ptr table 0xd8000 (by move id; motion_RunMoveScript 0x4e4a0, data ROM base 0xd0000000, script opcode switch fighter_ScriptOpcodeDispatchTail 0x44058); anim slot table 0xc4320 (fighter_LoadAnimSlot 0x4b7a0); move/state table 0xc5770 (fighter_UpdateMotionState 0x478c0); per-frame float deltas move_AdvanceFrameMotion 0x448f0; bone matrices tgp_MulBoneMatrices 0x4bd70; motion_AdvanceKeyframe 0x4e890.

## Round 4 (10-29) hands/feet
- Exe (fighter_LoadPostureTable @060526c4): upper arm/thigh [0] = T(base) Ry(yaw) Rx(pitch) Rz(swivel p[0xf]) ...; forearm/shin [0xc] adds RotateByMac(p[0xc..0xe]) local translation; hand/foot [4] = T(target) RotateA(-facing) RotateC(f2) RotateA(f1) RotateB(f0) = ABSOLUTE in fighter frame (not forearm/shin relative). Swivel = 4th quad value = roll of bend plane about aim axis.
- Code: pose() now absolute hand/foot via trot(fs=(1,-1,-1)), swivel pole via aimpole() (env DOA_SWA/DOA_HFS/DOA_FFS; DOA_NOSW, DOA_REL = v3 behaviour). Wrist clamp 75 deg (DOA_WLIM) toward forearm axis.
- Check: tools/doa_bayman_check.py (wrist angle, sole tilt, worst frames). v3: wrist mean 109 max 177, 702/962 frames >90; idle wrist 140/129. v4: mean 44 max 75, 0 >90; idle 23/26; idle sole tilt 13/12, sole y 0.00. Unclamped abs sign (1,-1,-1) alone: mean 54, 181 frames >90 (m015, m188 worst; cause unknown, maybe elbow IK).
- m195 = VICTIM of a throw (hands overhead, body airborne, ends supine), NOT Bayman's own throw; root/pelvis fine. Not a bug.
- Sheets: marks/bayman_anims_v4.png, bayman_handsfeet_v4.png. Frame-sign of trunk fields (1,1,1) vs hands (1,-1,-1) inconsistency unresolved.

## Arcade anims (10-29)
Tool C:\goobi\tools\doa_arcade_anim.py -> assets\anim3d\bayman_arcade_anim.glb (15-bone armature, rigid parts, 22 clips, 60 keys/s); sheet marks\bayman_arcade_anims_v1.png. (m2rom.load_data now applies ROM_COPY 0x1800000->0x1c00000.)
- main_data map: 0x06xxxxxx -> offset a-0x6000000+0x1000000. Table base = u32@0x1000000. Motion i<0x552: Q=u32[a2o(base)+4i]; i>=0x552: base2=u32[a2o(0x6c00004)], idx i-0x552. 1947 motions.
- Q = 16 u32 ptrs at END of motion data: p0..14 = streams (F x 3 s16, 65536=360deg), p15 = root triples (F x xyz float32, end marker 4.29e9). Frame0 root absolute (y=hip height .68 idle), later = deltas (cumsum used).
- Stream order: chest head hip footR foreR handR thighR shinR upperR footL foreL handL thighL shinL upperL. Every part has explicit angles (no IK).
- Bayman = motions 1362..1571 (move scripts group 8, prog.bin 0xd8000 ptr table, array 0xdb070). Proof: Saturn idle trunk == arcade 1362 with y sign flipped. No names in ROM; clip names are guesses from poses.
- Convention (verified visually + numerically): M = Rz*Ry*Rx, field0->X, 1->Y, 2->Z, all three signs -1, same for L (no mirror); hierarchy hip>chest>head/upper>fore>hand, hip>thigh>shin>foot, offsets = Saturn node table. Saturn idle endpoints match arcade FK: Saturn stream0=handL, 1=handR, 2=footL, 3=footR; R=+x. Feet y~0 in idle.
- Caveats: 1517,1523,1527,1531,1404 are victim/knockdown reactions, not attacker throws (attacker throw not located; script opcodes 9,10,11 undecoded). Root deltas frame (world vs local) unverified. Hands are rigid fists/open per stream, no finger anim. 210 motions total, only 22 exported (stats in work\doa_arcade\anim\stats.txt).

## Arcade other fighters (10-29)
- Tools: C:\goobi\tools\doa_arcade_fighter.py (model script parametrised: name chest_id chunk tintjson), doa_fighters_build.py (all 9 + tints), doa_fighters_sheet.py (front sheet). Work: work\doa_arcade (blocks.py, edgescore.py, partscore.py, headgrid.py).
- Block layout identical to Bayman: chest id C, head C+1, hip +2, R foot/fore/hand/thigh/shin/upper +3..+8, L +9..+14; +15 placeholder, +16 accessory (tags only for Bayman, others 15 parts). 15 geometry signatures found; costume blocks share geometry.
- Texture chunk (k, 0x5c0000+k*0xc0000) per character found by texture-seam mismatch score (edgescore.py; Bayman=8 verified). Chest ids/chunks: kasumi 672/k1, tina 1584/k0, zack 2496/k2, hayabusa 4944/k4, genfu 8640/k6, ayane 9377/k7, raidou 10297/k0, jannlee 11369/k9, leifang 14104/k12. Names = visual guess (hair/outfit), unverified. Not exported: 3321/k3 (Kasumi variant), 2864, 3705, 5776, 7192 (blonde women, unsure), 10984/12633, 15104.
- Textures real detail (grayscale luma) + manual tints per character (palette still unresolved). Output assets\anim3d\doa_<name>.glb, sheet marks\doa_fighters_v1.png.

## Arcade data map (11-02)
Full table: arcade/ghidra/DATAMAP.md. Status: PARTIAL, not DONE.
- Jump tables: 78 found (ghidra/jtab.tsv), code behind them added: functions 1969 -> 1984 (15 DOA_orph_*, still unnamed = OPEN). Ghidra instr orphans 0.
- 342 "uncovered rets": 311 have no Ghidra instruction: 180 DATA (ldref proof), 97 JUNK + 31 PAD (heuristic, OPEN-low), 3 REVIEW (OPEN). 319 holes (data-as-code, 0x9d000-0xa1000, 0x71d30) OPEN.
- Fighter record 0x58 stride (P1 0x54fc00, P2 0x54fc58): ~31 fields PROVEN from debug strings (test_PrintPlayerDebug). OPEN: health, guard, anim frame; Ghidra struct not created (no RAM block in project).
- OPEN: camera struct layout, hit/hurt volume tables, stage id + select bytes, ai_ScriptInterpreter opcodes, move table 0x95750, globals naming (1877 RAM addrs, ~45 named).

### Arcade data map update (11-02, pass 2)
- Ghidra: WORKRAM block 0x500000-0x5fffff + struct Fighter(0x58) at 0x54fc00/0x54fc58 (SetupRam.java). Fighter +8 = pos_y (height, 1.0 on floor), not health; fall-out KO = Y<=0 in round_CheckKO. Health is not in the record: OPEN.
- Hit/hurt volumes mapped (DATAMAP.md): body spheres 0x5503c0, capsules 0x552610, attack spheres 0x552960, ROM ptr tables 0xc1090 / 0xc05f0 / 0xbf580, move hit entries 0x9cbe0[chr] (0x14 B each).
- 11 DOA_orph_* functions named by provenance (<parent>_case_/_tail_<addr>, semantics OPEN). Ret audit by instr.tsv: 41 rets without instruction (was 311 by the extent measure): 13 were reachable code, fixed; 4 reachable fallthrough rets (0x8b4c 0x8bbc 0x7a934 0x71e0c) still outside Ghidra bodies = OPEN; rest follow bx/b/ret or sit in zero padding (unreachable, no xref).
- Still OPEN: camera struct, stage id byte, select bytes, ai_ScriptInterpreter opcodes, move table 0x95750, health/guard/anim frame, ~1757 unnamed globals.

## 11-02 Saturn closure (saturnport/DATAMAP.md)
- Fighter offsets, D960 states, AI level closed; Mednafen floor matches ours; stage 7 = NBG2/NBG1 map regs point at empty VRAM (writer unidentified, blocker logged).
- 11-02 Saturn stage 7 closed: it is the Training room (mode byte 0x0600D7BC==5 picks stage 7 in fn 0603fb2c), not a render bug; VDP2 map math verified (0x7D000); V-blank-in DMA handler 060A02A6 unnamed in Ghidra. See saturnport/DATAMAP.md.

## Arcade data side, 11-02 night
Names applied in Ghidra project DOAarc (arcade/ghidra): 1247 globals PROVEN, 182 DEAD (zero read xref), 448 OPEN. 11 orphans named, 4 stray rets placed, AI opcodes (ai_opcodes.md) and move table (move_table.tsv, pair table 0x956f0) decoded. Live-proven: health, guard, round timer, camera, select bytes, stage id, move frame counter. Details: arcade/ghidra/DATAMAP.md. Repo: github.com/indieindie7/deadoralive-decomp arcade/. Still OPEN: see DATAMAP.md last section.

Arcade update 11-02 late: globals 1639 PROVEN / 239 DEAD / 0 OPEN; decomp_doaarc.c re-exported with names; see arcade/ghidra/DATAMAP.md.
