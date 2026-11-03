# live_r5: input bit3 + keyframe index (DOA arcade Model 2A)
Premise fix: P1 input byte 0x54fccd is NOT fighter+0xcd (stride 1: P2 = 0x54fcce); lies past fighter recs.
## 1. 0x54fccd bit3 (0x08) = UNUSED
- Sole writer: io_ReadAllInputs 0x08050, stob at 0x08174 (P2 0x08184). Port is active-low; word inverted at 0x081ac.
- Readers 0x4854..0x88d14 (list in prog.dis grep) test only punch/kick/dirs/hold; no tester of mask 0x08 found; input test screen 0x87da0 only echoes.
- Live: punch -> 0x02, kick -> 0x04; bit3 never set in any dumped frame (2680-2800).
- Verdict: unused bit, written by io_ReadAllInputs 0x08174. Not proven absent in all menus (static scan only).
## 2. Keyframe index = u32 0x56ada8 (P1), 0x56adac (P2)
- Advance: st +1 at 0x44a10 and 0x44c4c (move_AdvanceFrameMotion); init at 0x42648/0x4290c.
- Live: steps +1/frame through the punch.
- NOT proven: exact start index source (idx=4 for move 83), stores at 0x4e618/0x4e8e8.
See live_r5.tsv (Y = direct evidence, N = static only).
