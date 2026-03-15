# HeroAgent

HeroAgent 是一个帮你定目标、拆计划、推进任务、验收结果、复盘问题并维护知识的工作流 skill。

它适合处理三类问题：

- 把模糊意图收敛为明确目标、计划和任务
- 在多轮推进中维护当前状态、完成记录和验收结论
- 把项目知识、复盘结论和流程标准沉淀下来

如果你只是在做一次性编码、修 bug 或临时问答，而不需要目标推进或知识沉淀，通常不需要使用 HeroAgent。

## 安装

推荐使用 `npx skills add` 安装：

```bash
npx skills add xiaozuoyou/heroagent
```

安装后可用以下命令确认：

```bash
npx skills list
```

如果需要更新，重新执行安装命令即可，也可以使用：

```bash
npx skills update
```

## 它解决什么问题

HeroAgent 把日常工作拆成三层：

- 初始化与知识：`init`、`wiki`
- 目标推进：`want -> plan -> todo -> achieve | abandon`
- 状态观察：`focus`
- 问题复盘：`reflect`

另外还有一组内部沉淀方法：

- `realize`：把确认过的复盘结论写成原则
- `synthesize`：压缩长记录、提炼一句话经验、合并重复知识
- `forget`：淘汰旧知识、旧需求结论和失效约束
- `master`：固化 HeroAgent 或项目级执行标准

## 核心能力

### 目标推进

- `want`：把模糊意图收敛为明确目标
- `plan`：把目标拆成阶段路径
- `todo`：把路径落成可执行清单
- `focus`：查看当前最重要的进展、阻塞和下一步
- `achieve`：判断目标是否真正达成
- `abandon`：在不值得继续时明确停损和收口

### 问题复盘

- `reflect`：基于材料复盘问题和根因

### 内部沉淀方法

- `realize`：仅在 `reflect` 结论被确认后使用
- `synthesize`：作为 `wiki` 的压缩整理方法使用
- `forget`：作为 `wiki` 的淘汰清理方法使用
- `master`：作为流程标准沉淀使用，不是常规用户动作

### 工作区与知识库

HeroAgent 支持在项目内维护 `.heroagent/` 工作区，包括：

- `goals/`、`plans/`、`tasks/`
- `progress/current-focus.md`
- `archive/`
- `wiki/`

其中 `processes/` 不是默认初始化目录，只在确实要沉淀稳定流程时按需创建。

其中 `.heroagent/wiki/` 用于维护项目知识，包括：

- `overview.md`
- `arch.md`
- `api.md`
- `data.md`
- `modules/`
- `index.md`
- `registry.json`
- `drafts/`

在 `want`、`plan`、`todo`、`focus`、`reflect` 等动作里，如果 wiki 已存在，HeroAgent 应优先消费它，而不是重新从零扫描项目。`reflect` 还应优先读取当前目标材料或归档材料，wiki 只负责补结构背景，不替代事件证据。

## 如何使用

正常使用时，你主要通过自然语言或 `~动作` 触发 HeroAgent，底层脚本应由 skill 自动选择，而不是让你手动敲命令。

典型说法例如：

- `我想把订单退款流程规范起来，先帮我定目标`
- `目标已经明确了，帮我拆一个两周计划`
- `把这个计划拆成可执行 todo`
- `我现在最该盯什么`
- `这批任务已经做完了，帮我看看现在能不能验收`
- `现在算达成了吗`
- `帮我复盘这次延期`
- `把支付模块的知识补到 wiki`
- `根据这轮改动同步 wiki`

默认情况下，HeroAgent 会按优先级连续执行整批 `todo`，只有遇到关键取舍、高风险操作或外部阻塞时才会停下来确认。
当整批 `todo` 完成后，HeroAgent 会先切到“已完成，待验收”的内部状态，再进入 `achieve` 判断是否真正收口。
如果过程中出现明显问题、返工或判断偏差，HeroAgent 应先用 `reflect` 复盘；复盘结论被确认后，再内部执行 `realize` 沉淀经验。

更完整的动作路由、输出规范和执行边界，请看：

- [SKILL.md](/Users/zuoyou/Documents/github/heroagent/SKILL.md)
- [command-routing.md](/Users/zuoyou/Documents/github/heroagent/references/command-routing.md)
- [output-contracts.md](/Users/zuoyou/Documents/github/heroagent/references/output-contracts.md)

## 推荐使用方式

### 方式一

只把 HeroAgent 当作对话型 skill 使用。

适合：

- 一次性需求澄清、规划或复盘
- 暂时不想落盘
- 先想把事情讲清楚，再决定是否进入长期工作区

推荐做法：

1. 直接调用 `$heroagent`
2. 用 `want`、`plan`、`todo`、`focus` 等动作推进
3. 在需要长期维护时，再初始化 `.heroagent/`

### 方式二

把 HeroAgent 当作长期工作流系统使用。

适合：

- 多轮推进同一个目标
- 需要持续维护计划、任务和焦点
- 需要让项目知识库跟着代码演进

推荐顺序：

1. 初始化工作区
2. 生成首批目标文件
3. 持续更新当前状态快照
4. 维护 wiki
5. 完成后归档

## 手动调试

上面的动作本来应该由 skill 自动触发。只有在你要调试、批处理、验证单个能力时，才建议直接运行 `scripts/*.py`。

### 显式指令

HeroAgent 同时支持自然语言触发和显式指令触发。

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

规则是：

- 显式指令优先级最高
- 没有显式指令时，再走自然语言识别

### 初始化指令

HeroAgent 内部支持 `init` 指令。

当你表达以下意图时，应该优先命中 `init`：

- 初始化当前项目
- 在老项目里接入 heroagent
- 开始长期落盘
- 自动创建 `.heroagent/`

命中后，推荐直接执行：

```bash
python3 scripts/init_heroagent.py /path/to/project
```

### 附带脚本

仓库内已经提供一组可执行脚本，主要用于调试、批处理和验证公开能力：

- `scripts/init_heroagent.py`：初始化 `.heroagent/`
- `scripts/bootstrap_first_goal.py`：生成首批目标、计划、任务草稿
- `scripts/update_current_focus.py`：更新 `current-focus.md`
- `scripts/archive_goal.py`：归档已完成或已放弃目标
- `scripts/doctor_heroagent.py`：检查工作区是否健康
- `scripts/update_want_state.py`：更新 `want` 阶段的评分、问题和移交流转状态
- `scripts/update_wiki_context.py`：更新 `.heroagent/wiki/` 知识文件
- `scripts/suggest_wiki_updates.py`：根据变更文件推导应同步的 wiki 文件
- `scripts/refresh_wiki_registry.py`：刷新 wiki 索引、注册表与新鲜度状态
- `scripts/sync_wiki_from_changes.py`：根据变更文件生成待补写草稿并刷新索引
- `scripts/apply_wiki_draft.py`：把待补写草稿合并进正式 wiki 并刷新索引
- `scripts/reconcile_wiki_state.py`：检查 wiki 草稿覆盖度、陈旧度与可合并状态
- `scripts/promote_wiki_maintenance.py`：按策略自动收敛 wiki 维护债务
- `scripts/compact_wiki_memory.py`：压缩正式 wiki 中重复的自动补充内容
- `scripts/score_wiki_signals.py`：给 wiki 打维护优先级和上下文价值分
- `scripts/assemble_wiki_context.py`：按动作自动装配 wiki 上下文包
- `scripts/extract_wiki_facts.py`：从代码变更中提炼更稳定的 wiki 事实
- `scripts/run_wiki_strategy.py`：按策略统一运行整套 wiki 自动维护

其中 wiki 的轻判断状态更新属于 skill 内部机制，由 HeroAgent 在合适时机自动触发，不要求用户手动执行。

## 一个最小工作流示例

```bash
python3 scripts/init_heroagent.py /path/to/project

python3 scripts/bootstrap_first_goal.py "规范团队周报流程" /path/to/project --refresh-focus

python3 scripts/update_current_focus.py \
  --goal "规范团队周报流程" \
  --stage focus \
  --completed "已产出首批目标、计划、任务草稿" \
  --in-progress "补全目标边界与阶段计划" \
  --blockers "无" \
  --next-step "先明确周报成功标准" \
  /path/to/project

python3 scripts/archive_goal.py --slug goal-d348d219 --reset-focus /path/to/project
```

## 仓库结构

```text
heroagent/
├── SKILL.md
├── README.md
├── agents/
├── assets/
│   └── templates/
├── references/
└── scripts/
```

各部分职责：

- `SKILL.md`：skill 主入口，负责触发、路由和核心规则
- `references/`：详细路由、输出规范、文件约定和 wiki 规则
- `assets/templates/`：目标、计划、任务、复盘、原则、流程模板
- `scripts/`：初始化、状态维护、归档和 wiki 维护脚本

## 建议阅读顺序

第一次接触这个仓库，建议按这个顺序阅读：

1. `README.md`
2. `SKILL.md`
3. `references/`
4. `scripts/`
