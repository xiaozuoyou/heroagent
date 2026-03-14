---
name: heroagent
description: 目标驱动与认知沉淀工作流 skill，用于把模糊意图转成目标、计划、任务、进度和复盘结论。适用于用户要求制定目标、拆解计划、维护 todo、查看进度、完成验收、放弃目标、反思问题、总结原则、沉淀流程、传授知识或清理过时知识等场景。
---

# HeroAgent

## 概览

把用户请求放进两条闭环里执行：

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

如需更具体的状态字段、动作衔接规则和对话示例，按需读取：

- [`references/state-management.md`](./references/state-management.md)
- [`references/action-examples.md`](./references/action-examples.md)
- [`references/prompt-patterns.md`](./references/prompt-patterns.md)
- [`references/command-routing.md`](./references/command-routing.md)
- [`references/output-contracts.md`](./references/output-contracts.md)
- [`references/file-conventions.md`](./references/file-conventions.md)
- [`references/init-conventions.md`](./references/init-conventions.md)
- [`references/bootstrap-conventions.md`](./references/bootstrap-conventions.md)
- [`references/focus-update-conventions.md`](./references/focus-update-conventions.md)
- [`references/archive-conventions.md`](./references/archive-conventions.md)
- [`references/operating-playbook.md`](./references/operating-playbook.md)

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

## 推进闭环

### `want`

把模糊意图压缩成一个可判断是否达成的目标。

输出以下内容：

```md
## 目标卡片
- 目标：...
- 背景：...
- 价值：...
- 范围：...
- 不做什么：...
- 成功标准：...
- 约束：...
```

若用户表达的是愿望而非目标，主动补全成功标准和边界。

### `plan`

把目标拆成阶段，不直接展开成零碎任务。

输出以下内容：

```md
## 里程碑计划
1. 阶段：...
   产出：...
   风险：...
   完成标志：...
2. 阶段：...
```

优先体现先后依赖、关键路径和验收节点。

### `todo`

把计划转成可执行、可完成、可验证的任务。

输出以下内容：

```md
## 任务列表
- [ ] 任务名
  完成定义：...
  依赖：...
  优先级：高 | 中 | 低
```

拆解任务时遵守以下规则：

- 一个任务只对应一个明确结果
- 任务名使用动作开头
- 单个任务应能在一个稳定工作段内完成
- 无法立即执行的事项标记为依赖，不伪装成进行中

### `focus`

输出当前最值得关注的信息，不重放全部历史。

输出以下内容：

```md
## 进度快照
- 当前目标：...
- 当前阶段：...
- 已完成：...
- 进行中：...
- 阻塞：...
- 下一步：...
```

当任务过多时，只展示关键路径相关内容。

### `finish`

在任务完成时更新任务状态，并说明结果如何推动目标前进。

输出以下内容：

```md
## 完成记录
- 完成任务：...
- 完成证据：...
- 对目标的推进：...
- 新风险或新机会：...
- 下一步：...
```

若任务没有真正完成，不要为了保持节奏而误报完成。

### `achieve`

判断是否真正达成目标，而不是只看任务是否全部勾选。

输出以下内容：

```md
## 达成结论
- 目标：...
- 验收结果：已达成 | 部分达成 | 未达成
- 证据：...
- 剩余缺口：...
- 是否归档：是 | 否
```

若只是部分达成，明确缺口并回到 `plan` 或 `todo`。

### `abandon`

在目标不再值得推进时，明确停止，而不是无限拖延。

输出以下内容：

```md
## 放弃结论
- 放弃目标：...
- 放弃原因：...
- 已投入沉没成本：...
- 可保留资产：...
- 重启条件：...
```

放弃不是失败包装，必须说清楚原因和后续影响。

## 沉淀闭环

### `reflect`

围绕具体问题做复盘，优先解释为什么会发生。

输出以下内容：

```md
## 反思记录
- 现象：...
- 影响：...
- 根因：...
- 当时漏判了什么：...
- 下次如何更早发现：...
```

避免把表面症状当作根因。

### `realize`

从单次事件中抽出可迁移的原则。

输出以下内容：

```md
## 原则卡片
- 原则：...
- 触发信号：...
- 适用边界：...
- 推荐动作：...
- 反例：...
```

原则必须可判断、可应用，不能写成空泛价值观。

### `master`

把多次验证过的原则固化为流程。

输出以下内容：

```md
## 流程卡片
- 流程名：...
- 适用场景：...
- 入口条件：...
- 步骤：
  1. ...
  2. ...
  3. ...
- 出口条件：...
- 常见失败点：...
```

只有在做法已相对稳定时再沉淀成流程，避免过早流程化。

### `synthesize`

把原则或流程教给别人，确保对方能理解并复用。

输出以下内容：

```md
## 教学稿
- 教什么：...
- 适合对象：...
- 核心模型：...
- 示例：...
- 常见误解：...
- 一句话带走：...
```

优先用例子和对比解释，不只给定义。

### `forget`

显式淘汰过时知识，避免旧认知继续误导执行。

输出以下内容：

```md
## 淘汰记录
- 淘汰对象：...
- 过时原因：...
- 失效信号：...
- 替代认知或替代流程：...
- 迁移建议：...
```

若只是“不常用”而不是“已过时”，不要轻易遗忘。

## 选择规则

按以下顺序判断应执行哪个动作：

1. 还没有明确目标，执行 `want`
2. 已有目标但没有路径，执行 `plan`
3. 已有计划但没有执行单元，执行 `todo`
4. 用户询问当前状态，执行 `focus`
5. 用户反馈任务完成，执行 `finish`
6. 用户要求验收闭环，执行 `achieve`
7. 用户决定停止推进，执行 `abandon`
8. 用户回顾问题成因，执行 `reflect`
9. 用户希望提炼通用方法，执行 `realize`
10. 用户希望把方法固定下来，执行 `master`
11. 用户希望教会别人，执行 `synthesize`
12. 用户指出旧知识失效，执行 `forget`

若一次请求同时命中多个动作，先处理推进闭环中的阻塞动作，再处理沉淀闭环。

## 响应风格

保持语言简洁、明确、可执行。优先：

- 先给结论，再给依据
- 少讲术语，多讲动作
- 少给大而空的框架，多给当前可用结果
- 对未确认事项直接标注，不自行脑补

除非用户明确要求，不要引入复杂理论命名或冗长方法论。
