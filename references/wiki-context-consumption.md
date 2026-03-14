# Wiki 上下文消费参考

## 目的

规定 HeroAgent 如何把 `.heroagent/wiki/` 里的知识真正消费为工作上下文，而不是只把它当成静态文档。

## 使用规则

- 读取 wiki 时，优先提取与当前动作直接相关的信息
- 不要把整个 wiki 全量搬进上下文
- 优先抽取目标、边界、模块关系、API 约定、数据约束

## 动作映射

### `want`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`

目的：

- 避免重复问项目目标、已有模块边界、关键限制

### `plan`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `wiki/modules/*.md`

目的：

- 确定阶段路径、关键依赖、可影响模块

### `todo`

优先读取：

- `wiki/modules/*.md`
- `wiki/api.md`
- `wiki/data.md`

目的：

- 让任务拆解贴近真实模块与接口边界

### `focus`

优先读取：

- `wiki/overview.md`
- `wiki/arch.md`
- `progress/current-focus.md`

目的：

- 用项目背景辅助判断当前最值得关注的内容

### `reflect`

优先读取：

- `wiki/arch.md`
- `wiki/data.md`
- `wiki/modules/*.md`

目的：

- 用结构性背景辅助识别根因，而不是只看表面现象

## 输出要求

消费 wiki 后，不必向用户重复整段文档内容，只需显式说明：

- 已参考哪些知识
- 它们如何影响当前判断
