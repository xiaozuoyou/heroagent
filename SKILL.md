---
name: heroagent
description: 目标驱动与认知沉淀工作流 skill，用于把模糊意图转成目标、计划、任务、进度和复盘结论。适用于用户要求制定目标、拆解计划、维护 todo、查看进度、完成验收、放弃目标、反思问题、总结原则、沉淀流程、传授知识或清理过时知识等场景。
---

# HeroAgent

## 概览

把用户请求放进两条闭环里执行：

- **初始化动作**：`init`
- **推进闭环**：`want -> plan -> todo -> focus -> finish -> achieve | abandon`
- **沉淀闭环**：`reflect -> realize -> master -> synthesize -> forget`

优先保持单一主目标。若用户同时提出多个目标，先帮助用户区分主目标、并行目标、暂存目标，再继续推进。

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

### 固定回复头

使用 `heroagent` 时，回复的第一行必须单独输出：

```md
[HeroAgent]
```

无论执行哪个动作、是否追问澄清、是否落盘，第一行都不能省略，也不要添加其他前缀内容。

## 动作总览

### 初始化动作

| 动作 | 目的 | 标准输出 |
| --- | --- | --- |
| `init` | 初始化 `.heroagent/` 工作区 | 初始化结果 |

### 推进闭环

| 动作 | 目的 | 标准输出 |
| --- | --- | --- |
| `want` | 定义目标 | 目标卡片 |
| `plan` | 制定路径 | 里程碑计划 |
| `todo` | 形成执行单元 | 任务列表 |
| `focus` | 查看当前态势 | 进度快照 |
| `finish` | 完成任务并更新状态 | 完成记录 |
| `achieve` | 验证目标达成 | 达成结论 |
| `abandon` | 停止目标并收口 | 放弃结论 |

### 沉淀闭环

| 动作 | 目的 | 标准输出 |
| --- | --- | --- |
| `reflect` | 复盘问题 | 反思记录 |
| `realize` | 提炼原则 | 原则卡片 |
| `master` | 固化做法 | 流程卡片 |
| `synthesize` | 传授知识 | 教学稿 |
| `forget` | 清理过时认知 | 淘汰记录 |

按需读取以下资料，不要一次性全量加载：

- 状态与路由：
  [`references/state-management.md`](./references/state-management.md)
  [`references/command-routing.md`](./references/command-routing.md)
  [`references/action-examples.md`](./references/action-examples.md)
- 提问与输出规范：
  [`references/prompt-patterns.md`](./references/prompt-patterns.md)
  [`references/output-contracts.md`](./references/output-contracts.md)
- 落盘与归档：
  [`references/file-conventions.md`](./references/file-conventions.md)
  [`references/init-conventions.md`](./references/init-conventions.md)
  [`references/bootstrap-conventions.md`](./references/bootstrap-conventions.md)
  [`references/focus-update-conventions.md`](./references/focus-update-conventions.md)
  [`references/archive-conventions.md`](./references/archive-conventions.md)

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

## 动作执行

所有动作统一遵循：

- 路由判断：`references/command-routing.md`
- 提问策略：`references/prompt-patterns.md`
- 输出规范：`references/output-contracts.md`
- 落盘方式：`references/file-conventions.md`

### 初始化动作

- `init`：当用户要求初始化、接管老项目、建立 `.heroagent/` 工作区、开始长期落盘时，优先执行。
- 命中 `init` 时，不只解释步骤，应直接执行 `scripts/init_heroagent.py`。
- 若当前项目缺少 `.heroagent/` 且请求明显属于长期工作流，优先自动初始化，再继续 `want`、`plan` 或 `todo`。

### 推进闭环

- `want`：将愿望收敛为可验收目标，不提前替用户展开计划。
- `plan`：将目标拆成阶段路径，突出依赖、风险、关键路径。
- `todo`：将阶段路径落成可执行任务，任务应可完成、可验证、可排序。
- `focus`：只输出当前最值得关注的信息，不重复整段历史。
- `finish`：记录任务完成证据，并说明它如何推进目标。
- `achieve`：按目标层面验收，不把任务勾选等同于达成。
- `abandon`：明确停损、保留资产与重启条件，不做拖延式收口。

### 沉淀闭环

- `reflect`：先分现象、影响、根因，再给改进信号。
- `realize`：把单次经验提炼成可迁移原则，而不是空泛价值观。
- `master`：只在做法稳定后固化为流程，避免过早流程化。
- `synthesize`：以讲清楚、教出去为目标，优先用例子而不是定义。
- `forget`：显式淘汰失效知识，并给出替代认知或替代流程。

## 选择规则

按以下顺序判断应执行哪个动作：

1. 用户要求初始化工作区或当前项目缺少 `.heroagent/` 且请求明显属于长期工作流，执行 `init`
2. 还没有明确目标，执行 `want`
3. 已有目标但没有路径，执行 `plan`
4. 已有计划但没有执行单元，执行 `todo`
5. 用户询问当前状态，执行 `focus`
6. 用户反馈任务完成，执行 `finish`
7. 用户要求验收闭环，执行 `achieve`
8. 用户决定停止推进，执行 `abandon`
9. 用户回顾问题成因，执行 `reflect`
10. 用户希望提炼通用方法，执行 `realize`
11. 用户希望把方法固定下来，执行 `master`
12. 用户希望教会别人，执行 `synthesize`
13. 用户指出旧知识失效，执行 `forget`

若一次请求同时命中多个动作，先处理推进闭环中的阻塞动作，再处理沉淀闭环。

## 响应风格

保持语言简洁、明确、可执行。优先：

- 先给结论，再给依据
- 少讲术语，多讲动作
- 少给大而空的框架，多给当前可用结果
- 对未确认事项直接标注，不自行脑补

除非用户明确要求，不要引入复杂理论命名或冗长方法论。
