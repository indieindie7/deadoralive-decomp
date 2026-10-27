# Dead or Alive (Sega Saturn, Tecmo 1997) reverse-engineering notes and symbols

Hand-named function map, review inputs and tools for the Saturn port of **Dead or Alive** (Japan, T-3603G V1.002,
SH-2), the 3D fighter with the counter-hold system and the danger zone ring edges. Round 1 = one naming pass over
every function of the main program, then a review of every provisional name with its callers:

| Program | Functions | Hand-named | Still `provisional` |
|---|---|---|---|
| 00DOA.BIN (main program at 0x06004000) | 1,605 | 1,603 | 51 |

Review verdicts: 705 confirmed, 191 renamed, 51 left unsure. 0 placeholder (`FUN_`) names left.

Subsystems named: Sega GFS / CDC file system and streaming (`gfs_`, `cdc_`, `stm_`), VDP2 (`vdp2_`), sound (`snd_`),
pad input (`pad_`), maths and fixed point (`math_`, `fp_`), the fight loop and fighters (`fight_`, `fighter_`, `hit_`),
CPU opponent AI (`ai_`), camera (`cam_`, `camscr_`, `camtgt_`, `campos_`), HUD, effects, text, menus, character select
(`hud_`, `fx_`, `text_`, `menu_`, `charsel_`), game / mode flow (`game_`, `sys_`).

Same method as [astal-decomp](https://github.com/indieindie7/astal-decomp) and
[clockworkknight-decomp](https://github.com/indieindie7/clockworkknight-decomp): functions by SH-2 prologue scan,
a decompile dump cut into slices, each slice named from its code and strings (prompt in `ghidra/naming/`), names
applied as USER_DEFINED labels, then every provisional name re-read with its callers by a local model (prompt in
`ghidra/review/`, verdicts applied with `tools/srprovapply.py`).
Non-commercial, done for study and preservation (fighting game design reference).

**No game data is included**: no disc image, no executables, no decompiled C, no game text, no Ghidra database.
You need your own copy of the game to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | disc layout, Ghidra setup, the naming round, the review round, what comes next |
| `ghidra/hand_00DOA.txt` | hand names: `0x<addr> func <name> hand <comment>` (apply with ApplyNames.java from the Scorcher / AMOK repos, hand mode) |
| `ghidra/funcinfo_00DOA.tsv` | per-function export: `F` address name source size, `C` callees (string rows removed) |
| `ghidra/naming/prompt_DOA.txt` | the round-1 naming prompt |
| `ghidra/review/prompt_r1_doa.txt` | the provisional-review prompt |
| `ghidra/scripts/` | `FindSh2FunctionsMem.java` (SH-2 prologue scan in a raw image), `CreateAt.java`, `CsDumpAll.java` (decompile dump with headers) |
| `tools/` | `ckprovctx.py` (review contexts with callers), `srprovapply.py` (apply verdicts), `pubfuncinfo.py` (strip strings from the export) |

## Licence

Notes, names and tools: MIT (see `LICENSE`). Dead or Alive belongs to Koei Tecmo; nothing from the game is distributed here.
