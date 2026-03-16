# HeroAgent

HeroAgent 是一个围绕“目标推进”设计的 workflow skill。

## 安装

```bash
npx skills add xiaozuoyou/heroagent
```

## 触发场景

- 需要先收敛目标，再形成计划
- 需要基于已确认计划继续执行和验收
- 需要复盘问题或同步项目知识

## 最小链路

- `want`：收敛目标
- `plan`：收敛方案并写入本地计划文档
- 用户确认计划
- `todo`：按计划执行
- `achieve`：验收

辅助动作：

- `focus`
- `wiki`
- `reflect`

## 最小用法

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

## 工作区

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

## 调试脚本

仓库内已经提供一组可执行脚本，主要用于调试、批处理和验证公开能力：

- `scripts/init_heroagent.py`
- `scripts/bootstrap_first_goal.py`
- `scripts/update_current_focus.py`
- `scripts/archive_goal.py`
- `scripts/doctor_heroagent.py`
- `scripts/update_plan_state.py`
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

- 主规则：[SKILL.md](/Users/zuoyou/Documents/github/heroagent/SKILL.md)
- core 规则：[references/core/command-routing.md](/Users/zuoyou/Documents/github/heroagent/references/core/command-routing.md)
- wiki 规则：[references/wiki/wiki-sync-rules.md](/Users/zuoyou/Documents/github/heroagent/references/wiki/wiki-sync-rules.md)
- 示例：[examples/minimal-flows.md](/Users/zuoyou/Documents/github/heroagent/examples/minimal-flows.md)
