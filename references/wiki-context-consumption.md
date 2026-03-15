# Wiki 上下文消费参考

## 目的

规定 HeroAgent 如何把 `.heroagent/wiki/` 里的知识真正消费为工作上下文，而不是只把它当成静态文档。

## 使用规则

- 优先读取 `wiki/index.md` 或 `wiki/registry.json`，先判断该读什么
- 若存在信号分，优先读取 `priority_score` 高且 `density_score` 较高的文档
- 读取 wiki 时，优先提取与当前动作直接相关的信息
- 不要把整个 wiki 全量搬进上下文
- 优先抽取目标、边界、模块关系、API 约定、数据约束
- 若正式文档仍未更新，可补读 `wiki/drafts/` 作为待确认线索，但不要把草稿内容直接当成事实
- 若正式文档存在 `自动同步摘要`，优先读摘要，再决定是否需要往下读原始细节
- 不同动作应优先装配不同的上下文包，而不是复用同一套文件组合
- 若存在 `facts__*.md` 这类源码提炼草稿，优先把它当作比通用草稿更稳定的线索

## 动作映射

### `want`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`

目的：

- 避免重复问项目目标、已有模块边界、关键限制
- 若存在更高优先级的 `overview` 或 `arch`，优先选分数更高者

### `plan`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `wiki/modules/*.md`

目的：

- 确定阶段路径、关键依赖、可影响模块
- 模块文档可按 `priority_score` 选前几份，不必全读

### `todo`

优先读取：

- `wiki/modules/*.md`
- `wiki/api.md`
- `wiki/data.md`

目的：

- 让任务拆解贴近真实模块与接口边界
- 若某模块文档优先级高于 `api` 或 `data`，可优先补读对应模块

### `focus`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `progress/current-focus.md`

目的：

- 用项目背景辅助判断当前最值得关注的内容
- 若有 `current-focus.md`，应与 wiki 上下文一起消费
- `focus` 是观察动作，不承担主流程推进职责

### `reflect`

优先读取：

- 先按 [`references/reflect-context-rules.md`](./reflect-context-rules.md) 判断是当前目标、已归档目标，还是通用问题
- 再补读 `wiki/arch.md`
- `wiki/data.md`
- `wiki/modules/*.md`

目的：

- 先基于工作流材料还原问题经过，再用结构性背景辅助识别根因
- 正式 wiki 主要用于补边界、依赖和约束，不替代事件证据本身
- 当正式文档不足时，可允许带入高优先级草稿作为线索，但必须标成待确认

## 输出要求

消费 wiki 后，不必向用户重复整段文档内容，只需显式说明：

- 已参考哪些知识
- 它们如何影响当前判断

若同时发现代码事实与 wiki 不一致，应补充：

- 哪些 wiki 文件建议同步
- 是否已执行最小更新
