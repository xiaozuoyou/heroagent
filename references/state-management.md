# 状态管理参考

## 目的

在 `heroagent` 中，所有动作都围绕一份可重建的轻量状态运作。  
状态不要求全量长期记忆，但要求每轮回答都能让用户看懂当前处于哪里、为什么在这里、下一步该去哪里。

## 状态机字段

推荐优先维护以下字段：

- `current_goal`：当前主目标
- `current_object`：`goal | plan | task | issue | wiki`
- `current_stage`：`clarify | planning | executing | reviewing | archiving`
- `workflow_mode`：`interactive | continuous`
- `complexity_level`：`light | standard | deep`
- `stage_status`：当前阶段的细分状态，如 `clarifying`、`ready_for_plan`
- `progress`：已完成的关键事实
- `blockers`：阻塞、依赖、风险
- `next_action`：下一步最合理动作
- `evidence`：支持判断的证据

如果信息不足，至少保住：

- `current_goal`
- `current_stage`
- `next_action`

## 阶段与动作的关系

HeroAgent 要区分两层：

- **阶段**：`clarify | planning | executing | reviewing | archiving`
- **动作**：`want | plan | todo | focus | achieve | abandon | reflect | wiki`

不要把动作和阶段混成一个概念。

推荐映射：

| 动作 | 默认阶段 | 说明 |
| --- | --- | --- |
| `want` | `clarify` | 收敛目标 |
| `plan` | `planning` | 形成路径 |
| `todo` | `executing` | 拆任务并连续推进 |
| `focus` | 不独占阶段 | 这是观察动作，只读取和更新当前态势 |
| `achieve` | `reviewing` | 做验收判断 |
| `abandon` | `archiving` | 做停损与收口 |
| `reflect` | `reviewing` | 复盘问题与根因 |
| `wiki` | 视任务而定 | 维护或消费知识，不强绑定单一阶段 |

## 复杂度分流

每次进入推进闭环前，先判断复杂度：

- `light`
  - 目标基本清楚
  - 范围稳定
  - 不需要完整闭环
  - 优先给最小可执行结果

- `standard`
  - 需要清晰目标、计划、任务和验收
  - 默认进入 `want -> plan -> todo -> achieve | abandon`

- `deep`
  - 多目标冲突
  - 长期推进
  - 阻塞复杂
  - 需要复盘或知识治理
  - 强制补风险、证据、验收口径，必要时转入 `reflect` 或 `wiki`

复杂度不是按文本长短判断，而是按治理强度判断。

## 阶段切换规则

### 推进闭环

按以下方向推进：

- 目标不清，进入 `want`
- 目标已清但路径不清，进入 `plan`
- 路径已清但缺少执行单元，进入 `todo`
- `todo` 全部完成后，切到“已完成，待验收”的内部状态
- 用户要求验收结果，进入 `achieve`
- 用户明确停止推进，进入 `abandon`

`focus` 不在主闭环中。它只负责查看和刷新当前态势。

### 复盘与沉淀

按以下方向处理：

- 需要解释问题成因，进入 `reflect`
- `reflect` 结论经用户确认后，内部触发 `realize`
- 需要整理历史知识、压缩长记录或淘汰旧结论时，进入 `wiki`
- 当经验已上升为长期执行标准时，再内部触发 `master`

## 多动作命中时的处理

当用户一句话同时触发多个动作时，按以下优先级处理：

1. 先解决推进闭环中的阻塞动作
2. 再处理验收或停损动作
3. 再处理 `reflect` 或 `wiki`
4. 最后才处理内部沉淀方法

例如：

- “我想做一个新产品，先帮我拆计划，再顺便总结方法”
  先做 `want` 或 `plan`，等有实际经验后再决定是否进入 `reflect`
- “这个任务做完了，帮我验收并复盘”
  先更新完成状态，再做 `achieve`，最后做 `reflect`

## 打破静默规则

默认采用 `continuous` 连续推进模式。  
只有满足以下情况，才从连续推进切到用户确认：

- 关键取舍会改变目标边界
- 需要做高风险落盘或覆盖性修改
- 当前目标与已有状态明显冲突
- 外部依赖阻塞，无法继续执行
- 验收标准无法判断

若不满足上述条件，不要频繁打断。

## 状态更新要求

每次输出后，都要能回答清楚这四个问题：

- 我们现在在做什么
- 已经完成了什么
- 还差什么
- 下一步最该做什么

如果无法回答，说明状态还没有收敛，需要先补事实。

## Wiki 状态

若项目启用了 `.heroagent/wiki/`，建议把 wiki 是否需要同步也视为流程状态的一部分。

推荐至少维护以下字段：

- `wiki_status`：`fresh | needs_sync`
- `pending_wiki_targets`：当前待同步的 wiki 文件
- `last_wiki_detected_at`：最近一次做轻判断的时间
- `last_wiki_sync_at`：最近一次正式同步的时间

推荐策略：

- 默认在代码变更完成后再做低成本判断，标记是否 `needs_sync`
- `want`、`plan`、`todo` 默认不触发 wiki 判断，它们优先维护目标、计划、任务状态
- 到 `achieve` 或显式 `wiki` 请求时，再检查是否需要正式同步
- 若需求边界、架构约束或项目事实在讨论阶段被显式改写，也可以例外触发一次判断
- 若本轮只生成草稿但未写回正式 wiki，状态仍应保持 `needs_sync`
- 轻判断由 skill 内部自动触发，不要求用户手动执行脚本

## 常见错误

- 把“愿望”直接当作“目标”
- 把“任务完成”直接当作“目标达成”
- 把 `focus` 误当成主流程阶段
- 把“表面问题”直接当作“根因”
- 把一次偶然成功直接上升为“流程”
- 把不常用知识误判为过时知识
