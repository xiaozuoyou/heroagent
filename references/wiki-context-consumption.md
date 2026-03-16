# Wiki 上下文消费参考

## 目的

规定 HeroAgent 如何消费 `.heroagent/wiki/` 作为工作上下文。

## 使用规则

- 优先读取 `wiki/index.md` 或 `wiki/registry.json`，先判断该读什么
- 若存在信号分，优先读取 `priority_score` 高且 `density_score` 较高的文档
- 读取 wiki 时，优先提取与当前动作直接相关的信息
- 不全量加载整个 wiki
- 优先抽取目标、边界、模块关系、API 约定、数据约束
- 若正式文档仍未更新，可补读 `wiki/drafts/` 作为待确认线索
- 若正式文档存在 `自动同步摘要`，优先读摘要，再决定是否需要往下读原始细节
- 按动作装配不同的上下文包
- 若存在 `facts__*.md` 这类源码提炼草稿，优先把它当作比通用草稿更稳定的线索

## 动作映射

### `want`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`

执行重点：

- 补齐项目目标、已有模块边界、关键限制
- 若存在更高优先级的 `overview` 或 `arch`，优先选分数更高者

### `plan`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `wiki/modules/*.md`

执行重点：

- 确定阶段路径、关键依赖、可影响模块
- 模块文档可按 `priority_score` 选前几份

### `todo`

优先读取：

- `wiki/modules/*.md`
- `wiki/api.md`
- `wiki/data.md`

执行重点：

- 让执行动作贴近真实模块与接口边界
- 若某模块文档优先级高于 `api` 或 `data`，可优先补读对应模块

### `focus`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `progress/current-focus.md`

执行重点：

- 用项目背景辅助判断当前最值得关注的内容
- 若有 `current-focus.md`，与 wiki 一起消费
- `focus` 只输出观察结果

### `reflect`

优先读取：

- 先按 [`references/reflect-context-rules.md`](./reflect-context-rules.md) 判断是当前目标、已归档目标，还是通用问题
- 再补读 `wiki/arch.md`
- `wiki/data.md`
- `wiki/modules/*.md`

执行重点：

- 先基于工作流材料还原问题经过，再用结构性背景辅助识别根因
- 正式 wiki 用于补边界、依赖和约束
- 正式文档不足时，可带入高优先级草稿作为待确认线索

## 输出要求

消费 wiki 后，直接输出：

- 已参考哪些知识
- 它们如何影响当前判断

若同时发现代码事实与 wiki 不一致，应补充：

- 哪些 wiki 文件建议同步
- 是否已执行最小更新
