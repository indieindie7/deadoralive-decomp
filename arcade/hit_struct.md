# Hit block 0x557ec8..0x557f90 (arcade DOA)

Not one record: a set of per-player arrays (index 0=P1, 1=P2), elements 1, 2 or 4 bytes. Fighter record base 0x54fc00, stride 0x58. Most are save/restore copies of fighter fields around a hit. Live-checked on a hidden copy exe (two hits, frames 2940-3110 and 3190-3210, every frame diffed; P1 hits P2 at f2987, P2 hits P1 at f3196).

Index key: D = defender index, A = attacker index, P = player.

| addr | width | idx | name | meaning |
|---|---|---|---|---|
| 557ec8 | u32[2] | D | g_hit_combo_pend | running combo damage (ec8,ecc); flushed into 557ed0[p] at combo end |
| 557ed0 | u32[2] | D | g_hit_combo_total | settled combo total, -3/frame; fighter+0x26 = ed0+ec8 |
| 557f20 | u8[2] | D | g_hit_phase | 3 at hit apply, else attacksta mirror |
| 557f22 | u8[2] | D | g_hit_posture | 1 down/air class, 2 other, 0 class 1; damage multiplier input |
| 557f24 | u8[2] | A | g_hit_atk_move | moveid that landed (live 0x56, 0x58) |
| 557f28 | u32 | - | g_hit_dispatch_abort | 1 stops fighter_DispatchStates second pass (throws/holds) |
| 557f40 | u32[2] | P | g_fighter_land_latch | DownRecover once-latch |
| 557f48..56 | u8[2] each | D | g_hit_resp_* / g_hit_save_* | queued response: 48 moveid(+2a), 4a actcode(+2b), 4c (+2c)=ff, 4e class(+2d), 50 (+36)=1; saved 52 animeflip(+34), 54 beatsta(+3e), 56 skysta(+3f) |
| 557f58 | u32[2] | D | g_hit_save_drct | facing/knock dir fixed point; restored into drct+bodydrct (live 0x8000, 0x1af4) |
| 557f68 | u32[2] | P | g_fighter_turn_pending | turn-to-face pending (UpdateFacing_2) |
| 557f70 | u32[2] | P | g_hit_chain_flag | prev state class was 3 at attack start; blocks actcancel in ApplyAttack |
| 557f78 | u8[2][2] | P*2+age | g_hist_moveid | moveid history, written by fighter_ShiftMoveHistory (1 and 2 frames late) |
| 557f7c | u8[2][2] | P*2+age | g_hist_class | state class (+2d) history |
| 557f80 | u8[2] | D | g_hit_damagenum | copy of fighter+0x4b |
| 557f82 | u8[2] | A | g_hit_index | hit table row (stride 0x14 into 0x9cbe0 / 0x9d8c0 per chr) |
| 557f84 | u8[2] | A | g_hit_active | hit latched flag; cleared at next attack start |
| 557f90 | 12-byte rec | chr*0xc00+move*0xc | g_hit_buf_table | u16 x4 + u32 from motion scratch 5555ee..f8; loaded to 5555fc..555604 by hit_LoadHitBuffer. Empty live; hit_BuildHitBuffers has no static caller |

## Not hit data sharing the block (named round_ / fighter_ / hist_ on purpose)
- 557f2c round_init_latch, 557f30/34 round_pose_latch[2], 557f38/3c round_pose_var[2], 557f60 round_play_mode_copy (all round_MainFrameLoop / round_SelectWinPose / round_CheckKO).
- 557f68 turn pending, 557f78/7c histories (fighter_ShiftMoveHistory).
- ranking_UpdateNameEntry is misnamed for 557ec8..ed4: it does combo tracking (flush ec8 into ed0 when fighter+0x52/0x53/0x54 combo flags drop; decay -3/frame). Its ranking name entry is 557ee8+.

## Live sequence (hit 1, P1 punch 0x56 hits P2)
f2987 hit applied: 557f21=3, 557f24=0x56, response 557f49=0x36, 4d=ff, 4f=09, 51=1, 57=1, 5c=0x8000, 82=3, 84=1; P2 +0x22 pending set.
f2988 P2 pending dmg 0x20 (+0x24); f2989 P2 hp 160>128 (0x20), 557ecc=0x20, +0x26=0x20.
f3047 combo ends: 557ecc 0x20>0, 557ed4 takes it (0x1d after first -3), then -3/frame to 0 at f3057 with fighter+0x26 mirroring.
Hit 2 (P2 0x58 hits P1) f3196-3198: 557f20=3, 557f25=0x58, 557f48=0x12, 557f58=0x1af4, 557f83=5, hp 160>150, 557ec8=0x0a.

## Result
38 rows: 38 PROVEN, 0 DEAD, 0 OPEN. No row has zero read xrefs (array elements are read through indexed access). Static-only (no live change observed): 557f22, 557f28, 557f40, 557f70, 557f2c..3c, 557f60.
