# 文件约定参考

## 目的

定义 `heroagent` 的落盘目录和文件定位。

## 工作区结构

若任务需要落盘，优先写入 `.heroagent/`：

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

`processes/` 只在需要沉淀流程标准时按需创建。

## 文件映射

### `want`

- 目录：`.heroagent/goals/`
- 模板：`assets/templates/goal-card.md`
- 规则：只在目标已经收敛到可落卡时写入

### `plan`

- 目录：`.heroagent/plans/`
- 模板：`assets/templates/milestone-plan.md`
- 规则：
  - `plan` 收敛后必须写入本地
  - 这是 `todo` 的默认输入文档
  - 计划文档至少包含：
    - `计划概览`
    - `关键取舍`
    - `阶段路径`
    - `待确认`
    - `下一步`

### `todo`

- 目录：默认不强制落盘
- 可选目录：`.heroagent/tasks/`
- 可选模板：`assets/templates/todo-list.md`
- 规则：
  - `todo` 的输入是已确认计划
  - 需要执行留痕时，再写 `tasks/*.md`

### `focus`

- 目录：`.heroagent/progress/`
- 模板：`assets/templates/progress-snapshot.md`
- 规则：
  - 优先覆盖 `progress/current-focus.md`
- 需要保留历史态势时，再额外写快照

### `achieve`

- 目录：优先更新对应目标文件；必要时补到 `.heroagent/progress/`
- 规则：记录验收结论、缺口和收口建议

### `abandon`

- 目录：优先更新对应目标文件；必要时补到 `.heroagent/progress/`
- 规则：记录放弃原因、可保留资产和重启条件

### `reflect`

- 目录：`.heroagent/retros/`
- 模板：`assets/templates/retrospective.md`

### `realize`

- 目录：`.heroagent/principles/`
- 模板：`assets/templates/principle-card.md`
- 规则：只在复盘结论被确认后写入

## 命名规则

- 时间戳：`YYYYMMDDHHMM`
- `slug`：小写英文和连字符
- 同一主题尽量复用同一 `slug`

## 更新规则

- 优先更新已有同主题文件，避免重复创建
- 目标、计划、原则优先原地维护
- 执行留痕和进度快照允许按时间追加

## 归档规则

当目标已达成或已放弃，且相关文件不再频繁更新时，可归档到：

```text
.heroagent/archive/
```

优先归档：

- 原目标
- 最终计划
- 相关执行留痕
- 最终进度与验收结论
- 相关复盘与原则
