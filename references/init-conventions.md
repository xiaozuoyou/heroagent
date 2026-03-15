# 初始化约定参考

## 目的

定义 `heroagent` 首次进入一个项目时，`.heroagent/` 目录应该如何建立，避免每次初始化结构不一致。

## 适用时机

在以下场景优先初始化 `.heroagent/`：

- 用户明确要求把结果持续落盘
- 当前任务是长期推进，不是一次性问答
- 目标、计划、任务、复盘需要形成连续记录
- 用户明确要求“初始化”“接管老项目”“开始接入 heroagent”

如果任务只是单轮讨论，不强制创建 `.heroagent/`。

## 推荐目录结构

```text
.heroagent/
├── goals/
├── plans/
├── tasks/
├── progress/
├── retros/
├── principles/
└── archive/
```

## 初始化时应创建的基础文件

建议同时创建以下占位文件：

- `.heroagent/goals/.gitkeep`
- `.heroagent/plans/.gitkeep`
- `.heroagent/tasks/.gitkeep`
- `.heroagent/progress/.gitkeep`
- `.heroagent/retros/.gitkeep`
- `.heroagent/principles/.gitkeep`
- `.heroagent/archive/.gitkeep`

## 可选启动文件

如果用户希望进入持续工作模式，可额外创建：

- `.heroagent/README.md`
- `.heroagent/progress/current-focus.md`

推荐用途：

- `README.md`：说明目录用途与工作规则
- `current-focus.md`：记录当前主目标、阶段、阻塞与下一步

## 初始化原则

- 默认不覆盖已有文件
- 已存在目录时只补缺失项
- 若用户未指定初始化范围，先创建最小可用结构
- 初始化结果应可直接被 `want`、`plan`、`todo`、`focus` 等动作复用
- 命中初始化意图时，优先直接运行 `scripts/init_heroagent.py`，不要只口头说明步骤

## 最小可用结构

若只允许创建最少内容，至少创建：

```text
.heroagent/
├── goals/
├── plans/
├── tasks/
└── progress/
```

若后续进入流程标准沉淀场景，再按需创建：

```text
.heroagent/processes/
```

## 初始化后的推荐第一步

初始化完成后，优先执行以下动作之一：

1. 若目标不清，执行 `want`
2. 若目标已清，执行 `plan`
3. 若计划已清，执行 `todo`

不要只创建目录而不给出下一步。
