# Dead or Alive (Saturn) decomp notes

## Disc
- Japan release T-3603G V1.002 (1997-09-12), 24 tracks. Data track: 354 files.
- Main program `00DOA.BIN` (734,916 bytes) loads at 0x06004000 (IP first read address).
- Per-fighter files: `XX_DAT.BIN` (motion data) and `XXn_TEX/MDL/LAD/TNK.BIN` (textures, models), XX = two-letter fighter code (KS, LE, TN, LU, ZA, BY, RI, ...).

## Ghidra
- Import 00DOA.BIN as SH-2 big-endian (SuperH:BE:32:SH-2) at 0x06004000, no auto-analysis of data.
- `FindSh2FunctionsMem.java` finds functions by prologue scan; `CreateAt.java` adds missed entries; `CsDumpAll.java` writes the decompile dump.
- Result: 1,605 functions.

## Round 1 naming
- The dump was cut into 11 slices; each slice named with `ghidra/naming/prompt_DOA.txt`.
- 1,603 hand lines, 947 marked provisional, one duplicate name suffixed with its address.

## Round 1 review
- `tools/ckprovctx.py` builds, per provisional name, the function plus its callers; a local model judged each with `ghidra/review/prompt_r1_doa.txt` (CONFIRM / RENAME / UNSURE).
- `tools/srprovapply.py`: 705 confirmed, 191 renamed, 51 unsure (still provisional). 0 duplicate names, 0 `FUN_` left.

## Next
- Round 2 on the 51 unsure names.
- Other code on the disc (overlays, the 68000 sound driver).
- Cross-check against the Model 2 arcade program (i960).
