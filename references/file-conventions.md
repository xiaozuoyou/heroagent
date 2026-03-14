# 文件约定参考

## 目的

为 `heroagent` 的落盘结果定义统一目录、命名方式和更新规则，避免同一类产物分散失控。

## 根目录约定

若任务需要把结果写入项目目录，优先写入 `.heroagent/`。推荐结构如下：

```text
.heroagent/
├── goals/
├── plans/
├── tasks/
├── progress/
├── retros/
├── principles/
└── processes/
```

如果目标项目尚未创建 `.heroagent/`，且用户明确需要落盘，则先创建该目录结构。

## 文件映射

### `want`

建议目录：

- `.heroagent/goals/`

建议命名：

- `{YYYYMMDDHHMM}_{slug}.md`

建议内容：

- 使用 `assets/templates/goal-card.md`

### `plan`

建议目录：

- `.heroagent/plans/`

建议命名：

- `{YYYYMMDDHHMM}_{slug}.md`

建议内容：

- 使用 `assets/templates/milestone-plan.md`

### `todo`

建议目录：

- `.heroagent/tasks/`

建议命名：

- `{YYYYMMDDHHMM}_{slug}.md`

建议内容：

- 使用 `assets/templates/todo-list.md`

### `focus`

建议目录：

- `.heroagent/progress/`

建议命名：

- `{YYYYMMDDHHMM}_{slug}.md`

建议内容：

- 使用 `assets/templates/progress-snapshot.md`

### `finish`

建议目录：

- 优先更新对应 `tasks/` 文件
- 如需单独记录，可追加到 `.heroagent/progress/`

建议规则：

- 已完成任务优先原地更新状态
- 若产生重要决策，再单独生成进度快照

### `achieve`

建议目录：

- 优先更新对应 `goals/` 文件
- 如需单独结论，可写入 `.heroagent/progress/`

建议规则：

- 目标达成后，补充验收结论
- 若已归档，可把相关文件移动到 `archive/`

### `abandon`

建议目录：

- 优先更新对应 `goals/` 文件
- 也可在 `.heroagent/progress/` 留下停损结论

建议规则：

- 必须记录放弃原因与可保留资产

### `reflect`

建议目录：

- `.heroagent/retros/`

建议命名：

- `{YYYYMMDDHHMM}_{topic}-retro.md`

建议内容：

- 使用 `assets/templates/retrospective.md`

### `realize`

建议目录：

- `.heroagent/principles/`

建议命名：

- `{principle_slug}.md`

建议内容：

- 使用 `assets/templates/principle-card.md`

### `master`

建议目录：

- `.heroagent/processes/`

建议命名：

- `{process_slug}.md`

建议内容：

- 使用 `assets/templates/process-card.md`

### `synthesize`

建议目录：

- 视对象写入 `principles/` 或 `processes/`
- 若是独立讲解稿，可暂放 `.heroagent/progress/`

建议规则：

- 若教学内容来自已有原则或流程，优先链接原文件而不是重复造文档

### `forget`

建议目录：

- 优先更新原有 `principles/` 或 `processes/` 文件
- 必要时在 `.heroagent/retros/` 留下淘汰说明

建议规则：

- 不直接静默删除，优先标注失效与替代项

## 命名规则

- 时间戳使用 `YYYYMMDDHHMM`
- `slug` 使用小写英文和连字符
- 同一主题尽量复用同一 `slug`
- 文件名优先表达对象，不表达情绪
- 若标题无法安全转成英文 `slug`，使用稳定的安全回退 `slug`

## 更新规则

- 优先更新已有同主题文件，避免重复创建
- 只有在新阶段、新主题、新周期时才新建文件
- 复盘、原则、流程优先沉淀长期可复用内容
- 进度快照允许按时间追加，目标与流程优先原地维护

## 归档规则

当目标已达成或已放弃，且相关文件不再频繁更新时，可归档到：

```text
.heroagent/archive/
```

归档时优先保留：

- 原目标
- 最终计划
- 最终任务状态
- 达成结论或放弃结论
- 相关复盘与原则
