# 动作触发矩阵

## 使用规则

按下表决定每个动作更新什么对象，以及何时补 wiki 判断。

## 触发矩阵

| 动作 | 默认更新对象 | 默认是否触发 wiki 判断 | 执行 |
| --- | --- | --- | --- |
| `init` | `.heroagent/` 工作区 | 否 | 建基础结构 |
| `want` | `goals/`、`workflow-state.json` | 否 | 更新目标状态 |
| `plan` | `plans/`、`current-focus.md` | 否 | 更新计划与当前态势 |
| `todo` | `current-focus.md`、执行状态 | 否 | 更新执行状态；需要留痕时再补 `tasks/` |
| `focus` | `current-focus.md` | 否 | 更新当前态势 |
| `achieve` | 目标状态、进度、归档信息 | 是 | 验收前检查待同步知识 |
| `abandon` | 目标状态、进度、归档信息 | 否 | 更新停损与收口状态 |
| `reflect` | `retros/`、相关目标材料 | 否 | 更新复盘材料 |
| `wiki` | `.heroagent/wiki/` | 是 | 处理知识更新 |

## 补充规则

- `want`、`plan`、`todo` 主要维护工作流状态，不默认改 wiki
- 只有项目事实被显式改写时，才额外标记 `wiki_status = needs_sync`
- `todo` 的执行留痕不等于 wiki 变化
- `achieve` 前，应检查是否还有待同步知识
