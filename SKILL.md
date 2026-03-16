---
name: heroagent
description: 帮你定目标、拆计划、推进任务、验收结果、复盘问题并维护项目知识的工作流 skill，适用于目标推进、问题复盘和 wiki 维护。
---

# HeroAgent

## 适用场景

当用户要处理以下问题时，使用 `heroagent`：

- 把模糊意图收敛成明确目标
- 把目标继续收敛成一份可确认的本地计划
- 基于已确认计划持续执行并验收
- 复盘问题并沉淀稳定经验
- 维护 `.heroagent/wiki/` 项目知识库，并在推进时优先消费它

如果用户只是做一次性编码、排错或临时问答，不要强行进入 `heroagent` 工作流。

## 主流程

按以下方式路由：

- 用 `init` 建立工作区
- 用 `wiki` 读写项目知识
- 按 `want -> plan -> todo -> achieve | abandon` 推进目标
- 用 `focus` 查看当前态势
- 用 `reflect` 复盘问题

内部方法按能力处理，不作为常规公开动作：

- `realize`：把确认过的复盘结论写入 `.heroagent/principles/`
- `synthesize`：压缩 wiki 长记录，提炼稳定结论
- `forget`：淘汰失效知识、旧约束和旧结论
- `master`：沉淀项目级或 HeroAgent 级执行标准

处理 `focus` 时，只更新观察结果，不改变主流程推进决定。

## 状态机骨架

进入任一动作前，先重建最小状态：

- `CURRENT_OBJECT`：`goal | plan | task | issue | wiki`
- `CURRENT_STAGE`：`clarify | planning | executing | reviewing | archiving`
- `WORKFLOW_MODE`：`interactive | continuous`
- `COMPLEXITY_LEVEL`：`light | standard | deep`
- `NEXT_ACTION`：当前最合理的下一步
- `WIKI_SYNC_STATE`：`fresh | needs_sync | draft`

若信息不足，至少重建：

- 当前主目标
- 当前阶段
- 已知阻塞
- 下一步动作

优先根据当前对话和 `.heroagent/` 已有材料重建状态，不补造历史记忆。

## 复杂度分流

先判断复杂度，再决定流程强度：

| 等级 | 适用情况 | 默认处理 |
| --- | --- | --- |
| `light` | 目标基本清楚，只需轻澄清、轻规划或轻观察 | 给最小可执行结果，不强拉完整闭环 |
| `standard` | 需要目标、计划、执行、验收的标准推进 | 进入 `want -> plan -> todo -> achieve \| abandon` |
| `deep` | 多目标冲突、长期推进、阻塞复杂、需要复盘或知识治理 | 强制补事实、风险、证据和验收口径，必要时转 `reflect` 或 `wiki` |

复杂度优先看四件事：

- 目标是否清楚
- 范围是否稳定
- 是否需要长期状态维护
- 是否需要知识沉淀或复盘

## 动作路由

推荐优先使用显式指令：

- `~init`
- `~wiki`
- `~want`
- `~plan`
- `~todo`
- `~focus`
- `~achieve`
- `~abandon`
- `~reflect`

路由规则：

- 显式指令优先于自然语言推断
- 没有显式指令时，优先命中当前最阻塞的一步
- 推进、复盘、知识维护同时出现时，先处理推进链路中的阻塞动作
- 若无法稳定判断，先补 1 个最关键问题，不要一次追问多个维度

## 动作边界

### `want`

- 入口条件：用户在表达愿望、方向、想法，但还没有形成可验收目标
- 先按 [`references/requirement-scoring.md`](./references/requirement-scoring.md) 做 10 分制评分
- 阈值：`8`
- 执行要求：
  - 评分 `< 8` 时，只做目标澄清
  - 评分 `>= 8` 时，输出目标卡或等价的目标收敛结果
  - 达到阈值后，让用户在 `继续 ~plan`、`继续补充需求`、`暂不处理` 中选择

### `plan`

- 入口条件：目标已明确，但路线、阶段、取舍或风险还需要继续对齐
- 执行要求：
  - 先继续沟通，直到方案收敛
  - 收敛后，把计划写入 `.heroagent/plans/`
  - 计划文档至少覆盖方案边界、关键取舍、阶段路径、进入执行条件
  - 写完后等待用户确认
- 流转要求：
  - 计划未收敛时，继续留在 `plan`
  - 目标边界被重写时，回到 `want`
  - 用户确认计划后，进入 `todo`

### `todo`

- 入口条件：已存在并已确认的计划文档
- 执行要求：
  - 直接基于计划文档执行
  - 优先更新执行结果和状态
  - 需要留痕时，再补最小执行记录到 `tasks/`
  - 只有遇到关键取舍、高风险修改、权限受限、外部阻塞或需求边界变化时才暂停确认
- 流转要求：
  - 全部完成后，把内部状态切到“已完成，待验收”，下一步进入 `achieve`
  - 若发现计划本身仍有分歧，回到 `plan`

### `focus`

- 入口条件：用户在问当前状态、优先级、阻塞或下一步
- 执行要求：
  - 输出当前最值得关注的态势结论
  - 需要落盘时，更新 `progress/current-focus.md`
  - 只刷新观察结果，不顺手扩展成新规划
- 流转要求：若用户顺势要求重规划或验收，再转对应动作

### `achieve`

- 入口条件：任务已完成，或用户要求判断目标是否真正闭环
- 执行要求：
  - 输出验收结论、证据、缺口和收口建议
  - 证据不足时，保留未达成或部分达成结论
- 流转要求：
  - 已达成且适合收口，进入归档
  - 部分达成，回到 `todo`
  - 已失去继续价值，转入 `abandon`

### `abandon`

- 入口条件：用户明确停止推进、暂缓或放弃目标
- 执行要求：
  - 输出停损结论、可保留资产和重启条件
  - 直接收口，不转成规划讨论
- 流转要求：若用户改变决定，再回到 `want`、`plan` 或 `todo`

### `reflect`

- 入口条件：用户要复盘问题、偏差、延期、失误或根因
- 执行要求：
  - 先取证，再输出事实、判断、根因、漏判点、提前信号
  - 证据不足时，把不确定内容放入 `待确认`
- 流转要求：
  - 结论经用户确认后，可内部触发 `realize`
  - 若需要补结构背景，可消费 `wiki`
  - 若问题尚未解决，先回到推进闭环

### `wiki`

- 入口条件：用户要维护知识库、消费项目知识、压缩长记录或清理旧知识
- 执行要求：
  - 先消费现有 wiki，再决定是否补写
  - 生成草稿时，明确标注为待确认知识
  - `want`、`plan`、`todo` 默认只在项目事实被显式改写时触发 wiki 轻判断
- 流转要求：知识维护完成后结束；若同步后仍需继续推进，再转回对应动作

## 统一输出契约

所有正式输出优先固定为四段：

- `当前结论`
- `当前依据`
- `产物或状态更新`
- `下一步`

若需要用户决策，再补：

- `需要确认`

通用要求：

- 第一部分直接给结论
- 缺失信息明确标注，不伪造内容
- 需要用户决策时，优先给 2 到 3 个低成本选项，并包含 `暂不处理`
- 若需要落盘，优先与 `assets/templates/` 保持一致

详细契约按需读取 [`references/output-contracts.md`](./references/output-contracts.md)。

## 落盘规则

- `want`：可写入 `.heroagent/goals/`
- `plan`：必须写入 `.heroagent/plans/`
- `todo`：优先更新执行状态；如需留痕，再写入 `.heroagent/tasks/`
- `focus`：优先更新 `.heroagent/progress/current-focus.md`
- `reflect`：写入 `.heroagent/retros/`
- `realize`：写入 `.heroagent/principles/`

不要把执行留痕当作进入 `todo` 的前置条件。

## 按需加载

默认不要全量加载所有参考资料，只按场景读取：

- 路由与状态：
  [`references/command-routing.md`](./references/command-routing.md)
  [`references/state-management.md`](./references/state-management.md)
  [`references/complexity-routing.md`](./references/complexity-routing.md)
- 输出与提问：
  [`references/output-contracts.md`](./references/output-contracts.md)
  [`references/prompt-patterns.md`](./references/prompt-patterns.md)
  [`references/action-examples.md`](./references/action-examples.md)
- 落盘与初始化：
  [`references/file-conventions.md`](./references/file-conventions.md)
  [`references/init-conventions.md`](./references/init-conventions.md)
  [`references/bootstrap-conventions.md`](./references/bootstrap-conventions.md)
  [`references/archive-conventions.md`](./references/archive-conventions.md)
- wiki 与复盘：
  [`references/wiki-conventions.md`](./references/wiki-conventions.md)
  [`references/wiki-context-consumption.md`](./references/wiki-context-consumption.md)
  [`references/wiki-sync-rules.md`](./references/wiki-sync-rules.md)
  [`references/reflect-context-rules.md`](./references/reflect-context-rules.md)

如需直接落盘，优先复用：

- [`assets/templates/goal-card.md`](./assets/templates/goal-card.md)
- [`assets/templates/milestone-plan.md`](./assets/templates/milestone-plan.md)
- [`assets/templates/todo-list.md`](./assets/templates/todo-list.md)
- [`assets/templates/progress-snapshot.md`](./assets/templates/progress-snapshot.md)
- [`assets/templates/retrospective.md`](./assets/templates/retrospective.md)
- [`assets/templates/principle-card.md`](./assets/templates/principle-card.md)

## 优先脚本

只在需要落盘、批处理或巡检时调用脚本。优先使用：

- 初始化与状态：`scripts/init_heroagent.py`、`scripts/bootstrap_first_goal.py`、`scripts/update_current_focus.py`、`scripts/archive_goal.py`、`scripts/doctor_heroagent.py`
- `want` 状态：`scripts/update_want_state.py`
- wiki 维护：`scripts/update_wiki_context.py`、`scripts/suggest_wiki_updates.py`、`scripts/refresh_wiki_registry.py`
- wiki 草稿闭环：`scripts/sync_wiki_from_changes.py`、`scripts/apply_wiki_draft.py`、`scripts/reconcile_wiki_state.py`、`scripts/promote_wiki_maintenance.py`

wiki 轻判断属于内部机制，不要求用户手动调用脚本。

## 响应风格

保持语言简洁、明确、可执行。优先：

- 先给结论，再给依据
- 少讲理论，多给当前动作
- 不重复解释同一条规则
- 未确认事项直接标注，不自行脑补
