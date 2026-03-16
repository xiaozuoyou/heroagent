# 状态管理参考

## 目的

给 `heroagent` 提供一份轻量、可重建的状态骨架，服务推进链路：

- `want -> plan -> todo -> achieve | abandon`

## 最小状态

每次进入动作前，优先重建以下字段：

- `current_goal`
- `current_object`
- `active_plan_path`
- `plan_summary`
- `current_stage`
- `workflow_mode`
- `complexity_level`
- `stage_status`
- `next_action`
- `blockers`

若信息不足，至少保住：

- `current_goal`
- `current_stage`
- `next_action`

## 阶段与动作

阶段和动作必须分开：

| 动作 | 默认阶段 | 执行 |
| --- | --- | --- |
| `want` | `clarify` | 收敛目标 |
| `plan` | `planning` | 收敛方案并写计划文档 |
| `todo` | `executing` | 基于已确认计划开始执行 |
| `focus` | 不独占阶段 | 只观察当前态势 |
| `achieve` | `reviewing` | 做验收判断 |
| `abandon` | `archiving` | 做停损与收口 |
| `reflect` | `reviewing` | 复盘问题 |
| `wiki` | 视任务而定 | 消费或维护知识 |

处理 `focus` 时，不单独切换推进阶段。

## 推荐阶段状态

只保留真正有用的细分状态：

- `clarifying`
- `awaiting_goal_confirmation`
- `ready_for_plan`
- `planning`
- `plan_ready_for_confirm`
- `executing`
- `ready_for_review`
- `archived`
- `paused`

避免把计划确认和执行确认拆成额外的平行状态机。

## 推进切换

推荐按以下方向切换：

- 目标不清：进入 `want`
- 目标已基本成形但待用户确认：保持 `want`，切到 `awaiting_goal_confirmation`
- 目标已清但方案未收敛：进入 `plan`
- 进入 `plan` 时，先恢复 `active_plan_path`、计划摘要和当前焦点
- 计划文档已写完但待确认：保持 `planning`，并把 `stage_status` 设为 `plan_ready_for_confirm`，同时把 `next_action` 设为确认计划
- 用户确认计划后：进入 `todo`
- 执行完成：切到 `ready_for_review`
- 用户要求验收：进入 `achieve`
- 用户明确停止：进入 `abandon`

## 复杂度与模式

- `light`：给最小可执行结果，不强制完整闭环
- `standard`：按标准闭环推进
- `deep`：补事实、风险、证据和验收口径，必要时转 `reflect` 或 `wiki`

默认采用 `continuous` 连续推进模式。只有在以下情况才打断：

- 关键取舍会改变目标边界
- 高风险落盘或覆盖性修改
- 外部阻塞导致无法继续
- 验收标准无法判断

## wiki 状态

若项目启用了 `.heroagent/wiki/`，额外维护：

- `wiki_status`：`fresh | needs_sync`
- `pending_wiki_targets`
- `last_wiki_detected_at`
- `last_wiki_sync_at`

默认策略：

- `want`、`plan`、`todo` 主要更新工作流状态
- 只有项目事实被显式改写时，才额外标记 wiki 轻判断
- 到 `achieve` 或显式 `wiki` 请求时，再决定是否正式同步

## 常见错误

- 把“愿望”直接当作“目标”
- 把“任务完成”直接当作“目标达成”
- 把 `focus` 当成推进阶段
- 把 `todo` 理解成先生成任务文档再执行
- 把不确定判断写成确定事实
