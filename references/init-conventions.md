# 初始化约定参考

## 目的

定义 `.heroagent/` 的最小初始化结构。

## 适用时机

命中以下场景时优先初始化：

- 用户明确要求长期落盘
- 当前任务需要持续推进
- 用户明确说“初始化”“接管老项目”“开始接入 heroagent”

## 初始化结构

```text
.heroagent/
├── goals/
├── plans/
├── tasks/
├── progress/
├── retros/
├── principles/
├── archive/
└── wiki/
```

## 初始化原则

- 默认不覆盖已有文件
- 已存在目录时只补缺失项
- 初始化后应能直接承接 `want`、`plan`、`todo`
- 命中初始化意图时，优先直接运行 `scripts/init_heroagent.py`

## 可选文件

需要持续模式时，可额外创建：

- `.heroagent/README.md`
- `.heroagent/progress/current-focus.md`
- `.heroagent/progress/workflow-state.json`

## 初始化后的下一步

1. 目标不清，进入 `want`
2. 目标已清，进入 `plan`
3. 计划已确认，进入 `todo`
