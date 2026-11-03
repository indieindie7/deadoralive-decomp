# DOA arcade CPU AI state (0x563f90-0x564778), struct-of-arrays

No single struct: the AI is SoA, one array per field, indexed by player p (0/1, AI slot = g_ai_slot 0x5645b6).
Fighter record base 0x54fc00 + slot*0x58; own/opp pointers cached at 0x5645c0 / 0x5645c4.
Source: prog.dis. Rows: globals/r5out_ai.tsv.

## Task flow
- 0x25ca0 init; 0x25dcc per-frame loop: ai_ResetAll 26780, ai_UpdateFacing 26910, 56462c <- param record (25e08), per-player loops (snapshots, move-change detect 2606c, hist rings 26544-26724), frame counter 564768 (wrap 1000) at 26758.
- Script: ai_RunScriptStep 27190 -> ai_RunScriptFull 27820 (replay) ; ai_RunStateMachine 2a890 -> table walk (564624 cursor, 564630 abort) -> situation idx 564636 -> ai_StartMoveScript 2ae..; ai_RunScriptOpcode runs while 564638[p]=1; aiop_* advance 564778[p].

## Layout (stride = per player p unless noted)
| addr | stride | name | note |
|---|---|---|---|
| 563f90.. | 0x80/ring | g_ai_hist0..5 | history rings, head 564590 |
| 564590/91/92 | 1 | g_ai_hist_head / prev1 / prev2 | head, head-1, head-2 |
| 5645c0/c4 | 4 | g_ai_self_fighter / opp_fighter | fighter ptrs |
| 5645c8 | 1 | g_ai_move_fresh | 15-frame window |
| 5645ca | 1 | g_ai_move_change_pending | decision gate |
| 5645d6 | 1 | g_ai_frame_pick | this frame pick |
| 5645da | 1 | g_ai_last_started_move | |
| 5645dc | 1 | g_ai_last_pick_move | |
| 5645de | 1 | g_ai_replay_done | |
| 5645e2 | 1 | g_ai_replay_active | |
| 564624 | 4 | g_ai_tbl_cursor | |
| 564628 | 1 | g_ai_react_apply_flag | |
| 56462a | 1 | g_ai_react_kind (DEAD) | never written |
| 56462c | 4 | g_ai_param_rec_ptr | 0xa7d20 table |
| 564630 | 1 scalar | g_ai_tbl_abort | |
| 564632 | 1 | g_ai_sm_end_flag | |
| 564636 | 1 scalar | g_ai_situation_idx | 0..22 |
| 564638 | 1 | g_ai_script_active | |
| 564660 | 0x20 | g_ai_seq_step | [slot*0x20+entry] |
| 5646a0 | 0x20 | g_ai_seq_repeat_cnt | |
| 5646f0 | 16 | g_ai_move_hist | 16 entries |
| 564718 | 1 | g_ai_last_opp_move_def | |
| 564734 | 2 scalar | g_ai_timer_scale_base | 0x200 |
| 564738/3c/40 | 2 | g_ai_hitbuf_w0/1/2 | -> 564744 counter2 |
| 56474a | 1 | g_ai_script_param4a | |
| 564750 | 1 | g_ai_prev_f33 | |
| 564756, 56475c | scalar | prev mode copies | ResetAll triggers |
| 56475e / 564760 | 1 | g_ai_prev_f41 / f35 | |
| 564768 | 4 scalar | g_ai_task_frame_cnt | |
| 564778 | 1 | g_ai_script_step | |
| 564830/34 | 4 | g_hud_banner_active_p1/p2 | HUD, not AI |

DEAD (written only): 56474c, 564754, 564758, 5646e4; 56462a never written.
OPEN: 5647c0-564820 (15 rows) belong to fighter motion-state/ring-edge/knockback/camera code, not the AI; blocker = needs that subsystem's analysis.
Live confirm: not done.
