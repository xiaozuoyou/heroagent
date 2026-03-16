---
name: heroagent
description: 帮你定目标、拆计划、推进任务、验收结果、复盘问题并维护项目知识的工作流 skill，适用于目标推进、问题复盘和 wiki 维护。
---

# HeroAgent

## 触发场景

命中以下场景时使用 `heroagent`：

- 需要先收敛目标，再形成可确认计划
- 需要基于已确认计划继续执行并验收
- 需要复盘问题或维护 `.heroagent/wiki/`

如果当前请求只是一次性编码、排错或问答，不进入 `heroagent`。

## 主链路

- `~init`：初始化 `.heroagent/`
- `~wiki`：读写项目知识
- `~want`
- `~plan`
- `~todo`
- `~achieve`
- `~abandon`
- `~want -> ~plan -> ~todo -> ~achieve | ~abandon`
- `~focus`：查看当前态势
- `~reflect`：复盘问题

## 核心约束

### `want`

- 适用于目标、完成标准、边界或约束仍不稳定的场景
- `want` 只负责收敛目标，不负责写计划或开始执行
- `want` 的目标不是替用户单边判断需求，而是通过逐轮提问形成双方认可的目标定义
- 先消费当前项目上下文，再按 [`references/core/requirement-scoring.md`](./references/core/requirement-scoring.md) 评分
- 阈值是 `8`
- 分数只是当前共识成熟度的辅助评估，不替代用户确认
- 评分不足时，每轮只补 `1` 个最关键缺口
- 接近收敛但边界仍有分歧时，先给 `2` 到 `3` 个目标定义选项和取舍
- 每轮澄清后，都先复述当前理解，再让用户确认是否准确
- 达到阈值后，输出目标卡或等价目标收敛结果，但不直接进入 `plan`
- 用户明确选择 `~plan` 前，只停留在 `want`

<HARD-GATE>
在以下条件全部满足前，不得进入 `~plan`：
- 需求评分达到阈值
- 已形成可验收的目标定义
- 用户认可当前目标定义
- 用户明确选择进入 `~plan`

评分未达标时，只允许继续澄清。
不得替用户做关键取舍。
</HARD-GATE>

反模式：
不要因为任务看起来简单，就跳过 `want`。一句话需求、小改动、临时想法，也必须先确认目标、完成标准、边界和约束。

执行顺序：

1. 先查看当前项目上下文和已有目标线索
2. 给出当前理解，不把暂定理解当最终结论
3. 按评分规则判断还缺什么
4. 每轮只问 `1` 个最关键问题
5. 用户回答后，更新目标定义并请用户确认
6. 目标定义得到用户认可后，再给下一步选择

### `plan`

- 先继续沟通，直到方案收敛
- 进入 `plan` 前，先恢复当前计划上下文：优先读取 `.heroagent/plans/` 中当前计划、`.heroagent/progress/current-focus.md`、`.heroagent/progress/workflow-state.json`
- `plan` 不是只写一份静态文档，还要持续维护计划内的当前状态、已知事实、风险与失败记录
- 若连续完成若干轮搜索、阅读或对比，需及时把关键信息沉到计划文档，避免上下文漂移
- 同一做法连续失败时，不重复原动作；要把失败尝试和调整后的路径写进计划文档
- 收敛后，把计划写入 `.heroagent/plans/`
- 写完后等待用户确认
- 用户确认计划后，进入 `todo`

### `todo`

- 前提是已存在并已确认的计划文档
- 直接基于计划文档执行
- 需要留痕时，再补最小执行记录到 `tasks/`
- 不要把执行留痕当作进入 `todo` 的前置条件。

### `focus`

- 只输出当前态势
- 需要落盘时，更新 `progress/current-focus.md`

### `achieve`

- 先看证据，再给验收结论
- 证据不足时，不宣告达成

### `reflect`

- 先取证，再给判断
- 证据不足时，把不确定内容放入 `待确认`

### `wiki`

- 先消费现有 wiki，再决定是否补写
- 只在项目事实被显式改写时触发 wiki 轻判断
- `detect` 与 `sync` 关系按 [`references/wiki/wiki-sync-rules.md`](./references/wiki/wiki-sync-rules.md) 执行

## 输出槽位

所有正式输出优先固定为：

- `当前结论`
- `当前依据`
- `产物或状态更新`
- `下一步`

若需要用户决策，再补：

- `需要确认`

详细契约按需读取 [`references/core/output-contracts.md`](./references/core/output-contracts.md)。

## 落盘规则

- `plan` 必须写入 `.heroagent/plans/`
- `todo` 优先更新执行状态；需要留痕时再写入 `.heroagent/tasks/`
- `reflect` 写入 `.heroagent/retros/`
- `wiki` 写入 `.heroagent/wiki/`

## 按需加载

- core：
  [`references/core/command-routing.md`](./references/core/command-routing.md)
  [`references/core/state-management.md`](./references/core/state-management.md)
  [`references/core/complexity-routing.md`](./references/core/complexity-routing.md)
  [`references/core/output-contracts.md`](./references/core/output-contracts.md)
  [`references/core/prompt-patterns.md`](./references/core/prompt-patterns.md)
  [`references/core/file-conventions.md`](./references/core/file-conventions.md)
  [`references/core/init-conventions.md`](./references/core/init-conventions.md)
  [`references/core/archive-conventions.md`](./references/core/archive-conventions.md)
  [`references/core/reflect-context-rules.md`](./references/core/reflect-context-rules.md)
- wiki：
  [`references/wiki/wiki-conventions.md`](./references/wiki/wiki-conventions.md)
  [`references/wiki/wiki-context-consumption.md`](./references/wiki/wiki-context-consumption.md)
  [`references/wiki/wiki-sync-rules.md`](./references/wiki/wiki-sync-rules.md)
- examples：
  [`examples/minimal-flows.md`](./examples/minimal-flows.md)

## 脚本入口

- 工作区与状态：`scripts/init_heroagent.py`、`scripts/bootstrap_first_goal.py`、`scripts/update_current_focus.py`、`scripts/archive_goal.py`
- `want`：`scripts/update_want_state.py`
- wiki：`scripts/update_wiki_context.py`、`scripts/suggest_wiki_updates.py`、`scripts/refresh_wiki_registry.py`

wiki 轻判断属于内部机制，不要求用户手动调用。
