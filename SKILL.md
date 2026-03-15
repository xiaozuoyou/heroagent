---
name: heroagent
description: 目标驱动与认知沉淀工作流 skill，用于把模糊意图转成目标、计划、任务、进度和复盘结论。适用于用户要求制定目标、拆解计划、维护 todo、查看进度、完成验收、放弃目标、反思问题、总结原则、沉淀流程、传授知识或清理过时知识等场景。
---

# HeroAgent

## 概览

把用户请求放进两条闭环里执行：

- **初始化动作**：`init`
- **知识动作**：`wiki`
- **推进闭环**：`want -> plan -> todo -> focus -> finish -> achieve | abandon`
- **沉淀闭环**：`reflect -> realize -> master -> synthesize -> forget`

优先保持单一主目标。若用户同时提出多个目标，先帮助用户区分主目标、并行目标、暂存目标，再继续推进。

## 动作入口

默认推荐用 `~动作` 触发，对人和对 AI 都更稳定。

| 指令 | 目的 | 标准输出 |
| --- | --- | --- |
| `~init` | 初始化 `.heroagent/` 工作区 | 初始化结果 |
| `~wiki` | 维护并消费 `.heroagent/wiki/` 知识库 | Wiki 结果 |
| `~want` | 定义目标 | 目标卡片 |
| `~plan` | 制定路径 | 里程碑计划 |
| `~todo` | 形成执行单元 | 任务列表 |
| `~focus` | 查看当前态势 | 进度快照 |
| `~finish` | 完成任务并更新状态 | 完成记录 |
| `~achieve` | 验证目标达成 | 达成结论 |
| `~abandon` | 停止目标并收口 | 放弃结论 |
| `~reflect` | 复盘问题 | 反思记录 |
| `~realize` | 提炼原则 | 原则卡片 |
| `~master` | 固化做法 | 流程卡片 |
| `~synthesize` | 传授知识 | 教学稿 |
| `~forget` | 清理过时认知 | 淘汰记录 |

规则：

- 用户显式输入 `~动作` 时，直接命中对应动作
- 显式指令优先级高于自然语言路由
- 未使用显式指令时，再按自然语言进行动作判断
- 若用户是长期使用者，优先鼓励使用 `~动作`，减少误判

## 执行原则

### 先收敛，再展开

在进入任何动作前，先明确以下内容：

- 当前对象是什么：目标、计划、任务、问题、知识、流程
- 当前阶段是什么：新建、推进、复盘、归档、淘汰
- 成功标准是什么：完成定义、验收条件、停止条件

若关键信息缺失，先用最少的问题补齐；若可以安全假设，则明确假设后继续。

### 始终维护状态

始终在回答中显式维护一份轻量状态，至少包含：

- 当前目标
- 当前阶段
- 已知进展
- 下一步动作
- 风险或阻塞

若用户没有提供历史状态，先根据对话重建，不要假装存在外部记忆。

### 人类先看重点

默认把最重要的信息放在最前面，而不是把完整分析放在最前面。

- 先给 `重点摘要`
- 再给详细说明
- 再给 `下一步`
- 若确实需要用户决策，优先给编号选项

若用户没有回应某个选择，默认视为“暂不处理”，不要反复追问。

### 区分事实与判断

输出时区分三类信息：

- **事实**：用户已确认或已观察到的信息
- **判断**：基于事实得出的分析
- **待确认**：影响决策但尚未确认的信息

### 优先产出可执行结果

每个动作都要产出可直接使用的结果，避免停留在概念描述。优先给出：

- 清晰目标
- 可执行计划
- 可勾选任务
- 当前进度
- 复盘结论
- 可复用原则或流程

### 顶层输出头

使用 `heroagent` 时，回复首行应采用单行状态头，例如：

```md
✅ HeroAgent · 计划制定
❓ HeroAgent · 需要确认
⚠️ HeroAgent · 进度聚焦
💡 HeroAgent · 咨询问答
```

建议紧跟状态头先给：

```md
重点摘要：
- ...
- ...
```

按需读取以下资料，不要一次性全量加载：

- 状态与路由：
  [`references/state-management.md`](./references/state-management.md)
  [`references/command-routing.md`](./references/command-routing.md)
  [`references/action-examples.md`](./references/action-examples.md)
- 提问与输出规范：
  [`references/prompt-patterns.md`](./references/prompt-patterns.md)
  [`references/output-contracts.md`](./references/output-contracts.md)
  [`references/requirement-scoring.md`](./references/requirement-scoring.md)
- 落盘与归档：
  [`references/file-conventions.md`](./references/file-conventions.md)
  [`references/init-conventions.md`](./references/init-conventions.md)
  [`references/bootstrap-conventions.md`](./references/bootstrap-conventions.md)
  [`references/focus-update-conventions.md`](./references/focus-update-conventions.md)
  [`references/archive-conventions.md`](./references/archive-conventions.md)
  [`references/wiki-conventions.md`](./references/wiki-conventions.md)
  [`references/wiki-context-consumption.md`](./references/wiki-context-consumption.md)
  [`references/wiki-sync-rules.md`](./references/wiki-sync-rules.md)

如需直接落盘，优先复用：

- [`assets/templates/goal-card.md`](./assets/templates/goal-card.md)
- [`assets/templates/milestone-plan.md`](./assets/templates/milestone-plan.md)
- [`assets/templates/todo-list.md`](./assets/templates/todo-list.md)
- [`assets/templates/progress-snapshot.md`](./assets/templates/progress-snapshot.md)
- [`assets/templates/retrospective.md`](./assets/templates/retrospective.md)
- [`assets/templates/principle-card.md`](./assets/templates/principle-card.md)
- [`assets/templates/process-card.md`](./assets/templates/process-card.md)

如需初始化目标项目内的 `.heroagent/` 工作区，优先使用：

- [`scripts/init_heroagent.py`](./scripts/init_heroagent.py)
- [`scripts/bootstrap_first_goal.py`](./scripts/bootstrap_first_goal.py)
- [`scripts/update_current_focus.py`](./scripts/update_current_focus.py)
- [`scripts/archive_goal.py`](./scripts/archive_goal.py)
- [`scripts/doctor_heroagent.py`](./scripts/doctor_heroagent.py)
- [`scripts/update_wiki_context.py`](./scripts/update_wiki_context.py)
- [`scripts/suggest_wiki_updates.py`](./scripts/suggest_wiki_updates.py)
- [`scripts/refresh_wiki_registry.py`](./scripts/refresh_wiki_registry.py)
- [`scripts/sync_wiki_from_changes.py`](./scripts/sync_wiki_from_changes.py)
- [`scripts/apply_wiki_draft.py`](./scripts/apply_wiki_draft.py)
- [`scripts/reconcile_wiki_state.py`](./scripts/reconcile_wiki_state.py)
- [`scripts/promote_wiki_maintenance.py`](./scripts/promote_wiki_maintenance.py)
- [`scripts/compact_wiki_memory.py`](./scripts/compact_wiki_memory.py)
- [`scripts/score_wiki_signals.py`](./scripts/score_wiki_signals.py)
- [`scripts/assemble_wiki_context.py`](./scripts/assemble_wiki_context.py)
- [`scripts/extract_wiki_facts.py`](./scripts/extract_wiki_facts.py)
- [`scripts/run_wiki_strategy.py`](./scripts/run_wiki_strategy.py)
- [`scripts/update_want_state.py`](./scripts/update_want_state.py)

常用脚本分组：

- 初始化与状态：`init_heroagent`、`bootstrap_first_goal`、`update_current_focus`、`archive_goal`、`doctor_heroagent`
- want 收敛推进：`update_want_state`
- wiki 基础维护：`update_wiki_context`、`suggest_wiki_updates`、`refresh_wiki_registry`
- wiki 草稿闭环：`sync_wiki_from_changes`、`apply_wiki_draft`、`reconcile_wiki_state`、`promote_wiki_maintenance`
- wiki 优化增强：`compact_wiki_memory`、`score_wiki_signals`、`assemble_wiki_context`、`extract_wiki_facts`、`run_wiki_strategy`

## 动作执行

所有动作统一遵循：

- 路由判断：`references/command-routing.md`
- 提问策略：`references/prompt-patterns.md`
- 输出规范：`references/output-contracts.md`
- 落盘方式：`references/file-conventions.md`

### 初始化动作

- `~init`
  适用：初始化、接管老项目、建立 `.heroagent/`、开始长期落盘。
  执行：直接运行 `scripts/init_heroagent.py`。
  后续：初始化后再进入 `want`、`plan` 或 `todo`。

### 知识动作

- `wiki`：用于维护 `.heroagent/wiki/`，并把其中内容作为优先上下文来源。
- 当用户要求维护项目知识库、同步项目概览、补充架构/API/数据说明时，优先执行 `wiki`。
- `wiki` 支持核心知识文件与模块级知识文件，模块级文件位于 `.heroagent/wiki/modules/`。
- `wiki` 还应维护 AI 优先消费的 `index.md` 与 `registry.json`，用于标记文档状态、主题和建议同步项。
- 在 `want`、`plan`、`todo`、`focus`、`reflect` 等动作中，若 `.heroagent/wiki/` 存在，优先消费其内容，再决定是否继续追问或扫描代码。
- 命中 `wiki` 维护意图时，按以下顺序选择能力：
  1. 直接补写正文：`scripts/update_wiki_context.py`
  2. 先推导同步目标：`scripts/suggest_wiki_updates.py`
  3. 刷新索引与注册表：`scripts/refresh_wiki_registry.py`
  4. 生成待补写草稿：`scripts/sync_wiki_from_changes.py`
  5. 合并已确认草稿：`scripts/apply_wiki_draft.py`
  6. 巡检缺失草稿、陈旧草稿、可合并草稿：`scripts/reconcile_wiki_state.py`
  7. 自动收敛维护债务：`scripts/promote_wiki_maintenance.py`
  8. 压缩正式 wiki 噪音：`scripts/compact_wiki_memory.py`
  9. 计算维护优先级：`scripts/score_wiki_signals.py`
  10. 按动作装配上下文包：`scripts/assemble_wiki_context.py`
  11. 从代码提炼稳定事实：`scripts/extract_wiki_facts.py`
  12. 按 `conservative balanced aggressive` 统一运行：`scripts/run_wiki_strategy.py`

### 推进闭环

- `~want`
  目标：把愿望收敛为可验收目标，不提前展开计划。
  规则：先按 `references/requirement-scoring.md` 做 10 分制评分，阈值 8 分。
  提问：默认使用苏格拉底式单问单答，每轮只问 1 个最关键问题。
  边界：不允许替用户做关键取舍。
  补充：若有 wiki，先消费 `overview.md` 与 `arch.md`。
  收口：达到可进入下一步时，必须让用户选择 `继续 ~plan`、`继续补充需求` 或 `暂不处理`。
  状态：应把当前状态落到 `progress/workflow-state.json`，至少区分 `clarifying` 与 `ready_for_plan`。
- `~plan`
  目标：把目标拆成阶段路径，突出依赖、风险、关键路径。
  补充：优先消费 wiki 中的模块结构、架构关系与约束信息。
- `~todo`
  目标：把阶段路径落成可执行任务，保证可完成、可验证、可排序。
  补充：优先消费 wiki 中的模块、API、数据约束。
- `~focus`
  目标：只输出当前最值得关注的信息，不重复整段历史。
  补充：可结合 wiki 和 `current-focus.md` 共同判断当前重点。
- `~finish`
  目标：记录任务完成证据，并说明它如何推进目标。
- `~achieve`
  目标：按目标层面验收，不把任务勾选等同于达成。
- `~abandon`
  目标：明确停损、保留资产与重启条件，不做拖延式收口。

### 沉淀闭环

- `~reflect`
  目标：先分现象、影响、根因，再给改进信号。
- `~realize`
  目标：把单次经验提炼成可迁移原则，而不是空泛价值观。
- `~master`
  目标：只在做法稳定后固化为流程，避免过早流程化。
- `~synthesize`
  目标：以讲清楚、教出去为目标，优先用例子而不是定义。
- `~forget`
  目标：显式淘汰失效知识，并给出替代认知或替代流程。

## 选择规则

按以下顺序判断应执行哪个动作：

1. 用户要求初始化工作区或当前项目缺少 `.heroagent/` 且请求明显属于长期工作流，执行 `init`
2. 用户要求维护或更新项目知识库，执行 `wiki`
3. 还没有明确目标，执行 `want`
4. 已有目标但没有路径，执行 `plan`
5. 已有计划但没有执行单元，执行 `todo`
6. 用户询问当前状态，执行 `focus`
7. 用户反馈任务完成，执行 `finish`
8. 用户要求验收闭环，执行 `achieve`
9. 用户决定停止推进，执行 `abandon`
10. 用户回顾问题成因，执行 `reflect`
11. 用户希望提炼通用方法，执行 `realize`
12. 用户希望把方法固定下来，执行 `master`
13. 用户希望教会别人，执行 `synthesize`
14. 用户指出旧知识失效，执行 `forget`

若一次请求同时命中多个动作，先处理推进闭环中的阻塞动作，再处理沉淀闭环。

若 `want` 评分不足，则 `want` 本身先停在 `目标澄清`，不要直接进入 `plan`。

## 响应风格

保持语言简洁、明确、可执行。优先：

- 先给结论，再给依据
- 少讲术语，多讲动作
- 少给大而空的框架，多给当前可用结果
- 对未确认事项直接标注，不自行脑补

除非用户明确要求，不要引入复杂理论命名或冗长方法论。
