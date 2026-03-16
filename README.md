# HeroAgent

HeroAgent 是一个围绕“目标推进”设计的 workflow skill。

处理顺序：

- `want`：聊需求，收敛目标
- `plan`：继续沟通，收敛方案，并写入本地计划文档
- 用户确认计划
- `todo`：按计划文档开始执行
- `achieve`：验收
- `abandon`：停止推进并收口

- `focus`：查看当前态势
- `wiki`：读写项目知识
- `reflect`：复盘问题

## 安装

```bash
npx skills add xiaozuoyou/heroagent
```

安装后可执行：

```bash
npx skills list
```

## 触发场景

- 需要先收敛目标，再形成计划
- 需要基于已确认计划继续执行和验收
- 需要复盘问题或同步项目知识

## 核心动作

- 推进链路：`want -> plan -> todo -> achieve | abandon`
- 辅助动作：`focus`、`wiki`、`reflect`

## 最小用法

直接用自然语言或显式指令触发。

推荐显式指令：

- `~init`
- `~wiki`
- `~want`
- `~plan`
- `~todo`
- `~focus`
- `~achieve`
- `~abandon`
- `~reflect`

### 初始化指令

示例输入：

- `我想把退款流程规范起来，先帮我定目标`
- `目标明确了，帮我把方案收敛成计划`
- `计划确认了，直接开始执行`
- `我现在最该盯什么`
- `这批任务做完了，帮我看看能不能验收`
- `帮我复盘这次延期`
- `把支付模块的知识补到 wiki`

执行规则：

- `want` 先做需求完整度评分
- `plan` 先收敛方案，再写入 `.heroagent/plans/`
- `todo` 只在计划确认后执行
- `tasks/` 只承载执行留痕

## 工作区

需要长期维护状态时，使用 `.heroagent/`：

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

目录：

- `goals/`：目标卡
- `plans/`：已确认计划
- `tasks/`：执行留痕，可选
- `progress/`：当前态势与流程状态
- `retros/`：复盘记录
- `principles/`：稳定经验
- `archive/`：已达成或已放弃目标
- `wiki/`：项目知识库

## 调试脚本

只有在调试、批处理或显式落盘时，才直接执行脚本。

仓库内已经提供一组可执行脚本，主要用于调试、批处理和验证公开能力：

- `scripts/init_heroagent.py`
- `scripts/bootstrap_first_goal.py`
- `scripts/update_current_focus.py`
- `scripts/archive_goal.py`
- `scripts/doctor_heroagent.py`
- `scripts/update_want_state.py`
- `scripts/update_wiki_context.py`
- `scripts/suggest_wiki_updates.py`
- `scripts/refresh_wiki_registry.py`
- `scripts/sync_wiki_from_changes.py`
- `scripts/apply_wiki_draft.py`
- `scripts/reconcile_wiki_state.py`
- `scripts/promote_wiki_maintenance.py`
- `scripts/compact_wiki_memory.py`
- `scripts/score_wiki_signals.py`
- `scripts/assemble_wiki_context.py`
- `scripts/extract_wiki_facts.py`
- `scripts/run_wiki_strategy.py`

## 规则入口

主规则见 [SKILL.md](/Users/zuoyou/Documents/github/heroagent/SKILL.md)。

按需补充阅读：

- [command-routing.md](/Users/zuoyou/Documents/github/heroagent/references/command-routing.md)
- [state-management.md](/Users/zuoyou/Documents/github/heroagent/references/state-management.md)
- [output-contracts.md](/Users/zuoyou/Documents/github/heroagent/references/output-contracts.md)
- [file-conventions.md](/Users/zuoyou/Documents/github/heroagent/references/file-conventions.md)
