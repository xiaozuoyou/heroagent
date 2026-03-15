# HeroAgent

HeroAgent 是一个面向目标推进与认知沉淀的工作流智能体 skill。

它把日常工作拆成两条闭环：

- 初始化与知识：`init`、`wiki`
- 推进闭环：`want -> plan -> todo -> focus -> finish -> achieve | abandon`
- 沉淀闭环：`reflect -> realize -> master -> synthesize -> forget`

适合用于目标定义、阶段规划、任务拆解、进度聚焦、复盘总结、原则沉淀、流程固化，以及长期工作流的持续落盘。

## 安装

推荐使用 `npx skills add` 安装。

```bash
npx skills add xiaozuoyou/heroagent
```

### 安装后检查

```bash
npx skills list
```

如果需要更新，重新执行一次安装命令即可，或者`npx skills update`。

## 核心能力

### 目标推进

- `want`：把模糊意图收敛成明确目标
- `plan`：把目标拆成阶段路径
- `todo`：把阶段路径落成任务清单
- `focus`：查看当前目标、阶段、阻塞与下一步
- `finish`：记录任务完成情况
- `achieve`：判断目标是否真正达成
- `abandon`：在不值得继续时明确停损

### 认知沉淀

- `reflect`：复盘问题与根因
- `realize`：提炼可迁移原则
- `master`：把原则固化为流程
- `synthesize`：把知识讲清楚、教出去
- `forget`：清理过时知识与旧流程

### 工作区落盘

HeroAgent 支持在目标项目内维护 `.heroagent/` 工作区，沉淀以下内容：

- 目标卡片
- 里程碑计划
- 任务列表
- 当前焦点
- 复盘记录
- 原则卡片
- 流程卡片
- 归档结果

### Wiki 知识库

HeroAgent 现在支持 `.heroagent/wiki/`：

- `index.md`
- `registry.json`
- `drafts/`
- `overview.md`
- `arch.md`
- `api.md`
- `data.md`
- `modules/`

这部分不只是存储项目知识，还会在 `want`、`plan`、`todo`、`focus`、`reflect` 等动作中被优先消费为上下文。

其中：

- `index.md` 给 AI 提供优先阅读顺序和文档状态
- `registry.json` 提供结构化元信息，适合程序与 AI 消费
- `drafts/` 用于存放根据代码变更自动生成的待补写草稿

其中 `modules/` 用于沉淀模块级知识，建议一模块一文件，例如：

- `modules/payments.md`
- `modules/auth.md`
- `modules/reporting.md`

如果你刚完成一轮代码改动，建议先推导这次应同步哪些 wiki：

```bash
python3 scripts/suggest_wiki_updates.py \
  src/payments/service.ts \
  src/api/routes/orders.ts \
  prisma/schema.prisma
```

这一步适合：

- 刚做完功能开发或重构
- 刚改过接口、数据结构或模块边界
- 不确定应该更新哪份 wiki

如果你已经明确要更新某个模块，也可以直接写入模块级 wiki：

```bash
python3 scripts/update_wiki_context.py \
  --module payments \
  --content "## 新增说明\n\n- 支付模块负责统一收单与退款编排" \
  /path/to/project
```

如果你希望在代码变更后刷新整个 wiki 索引与新鲜度状态，可以执行：

```bash
python3 scripts/refresh_wiki_registry.py \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --changed-path prisma/schema.prisma \
  --materialize-suggestions \
  /path/to/project
```

如果你希望进一步根据代码变更自动生成待补写草稿，可以执行：

```bash
python3 scripts/sync_wiki_from_changes.py \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --changed-path prisma/schema.prisma \
  --materialize-suggestions \
  /path/to/project
```

它不会直接改正文，而是先在 `.heroagent/wiki/drafts/` 里生成候选草稿，适合 AI 继续完善。

如果你确认某份草稿已经可以并入正式 wiki，可以执行：

```bash
python3 scripts/apply_wiki_draft.py \
  modules__payments.md \
  /path/to/project
```

它会把草稿内容追加到对应正式 wiki，并自动刷新 `index.md` 与 `registry.json`。默认会删除已应用草稿，如需保留可加 `--keep-draft`。

如果你希望周期性检查 wiki 的维护状态，可以执行：

```bash
python3 scripts/reconcile_wiki_state.py \
  --changed-path src/payments/service.ts \
  --changed-path prisma/schema.prisma \
  --stale-days 7 \
  /path/to/project
```

它会在 `.heroagent/wiki/drafts/maintenance-report.md` 里写出维护报告，说明：

- 哪些目标 wiki 还没生成草稿
- 哪些草稿已经陈旧
- 哪些草稿可以直接合并

如果你希望按策略自动收敛这些维护债务，可以执行：

```bash
python3 scripts/promote_wiki_maintenance.py \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --materialize-missing \
  --apply-ready \
  --mark-stale \
  /path/to/project
```

它会：

- 为缺失目标自动补生成草稿
- 把可合并草稿并入正式 wiki
- 给陈旧草稿追加陈旧标记
- 最后刷新索引和注册表

如果正式 wiki 因多次自动补充变得过长，可以执行：

```bash
python3 scripts/compact_wiki_memory.py \
  --scope all \
  /path/to/project
```

它会把多个 `自动同步补充` 压成一个 `自动同步摘要`，更适合 AI 快速读取。

如果你希望知道当前最值得优先维护或优先读取的 wiki，可以执行：

```bash
python3 scripts/score_wiki_signals.py \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --top 5 \
  /path/to/project
```

它会输出每份 wiki 的信号分，包括：

- `priority`
- `freshness`
- `density`
- `draft_dependency`

如果你希望根据当前动作直接装配可用的 wiki 上下文包，可以执行：

```bash
python3 scripts/assemble_wiki_context.py \
  todo \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --limit 5 \
  /path/to/project
```

它会按动作语义、信号分和文档类型，自动挑选最适合的 wiki 子集。

如果你希望从代码变更里直接提炼更稳定的知识线索，可以执行：

```bash
python3 scripts/extract_wiki_facts.py \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --changed-path prisma/schema.prisma \
  /path/to/project
```

它会在 `wiki/drafts/` 下生成 `facts__*.md`，用于沉淀更稳定的源码事实，而不只是生成通用草稿。

如果你希望按统一策略来运行整套 wiki 自动维护，可以执行：

```bash
python3 scripts/run_wiki_strategy.py \
  balanced \
  --changed-path src/payments/service.ts \
  --changed-path src/api/routes/orders.ts \
  --changed-path prisma/schema.prisma \
  /path/to/project
```

当前支持 3 种策略：

- `conservative`
  只刷新索引和状态，不主动做高侵入动作
- `balanced`
  自动补草稿、标记陈旧草稿、提炼源码事实，但不自动合并正式 wiki
- `aggressive`
  自动补草稿、自动合并、自动提炼事实、自动压缩正式 wiki

### 显式指令

HeroAgent 同时支持自然语言触发和显式指令触发。

推荐显式指令：

- `~init`
- `~wiki`
- `~want`
- `~plan`
- `~todo`
- `~focus`
- `~finish`
- `~achieve`
- `~abandon`
- `~reflect`
- `~realize`
- `~master`
- `~synthesize`
- `~forget`

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

仓库内已经提供一组可执行脚本：

- `scripts/init_heroagent.py`：初始化 `.heroagent/`
- `scripts/bootstrap_first_goal.py`：生成首批目标、计划、任务草稿
- `scripts/update_current_focus.py`：更新 `current-focus.md`
- `scripts/archive_goal.py`：归档已完成或已放弃目标
- `scripts/doctor_heroagent.py`：检查工作区是否健康
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

## 推荐使用方式

### 方式一

只把 HeroAgent 当作对话型 skill 使用。

适合：

- 想快速讨论目标
- 不想把结果写入文件
- 只需要一次性分析、规划或复盘

推荐做法：

1. 直接调用 `$heroagent`
2. 用 `want plan todo focus` 等动作推进
3. 在需要时再决定是否落盘

### 方式二

把 HeroAgent 当作长期工作流系统使用。

适合：

- 多轮推进同一个目标
- 需要保留计划与任务状态
- 需要持续维护进度与归档

推荐顺序：

1. 初始化工作区
2. 生成首批目标文件
3. 持续更新当前焦点
4. 完成后归档

示例：

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

## 建议的使用习惯

- 先用 `want` 收边界，再进入 `plan`
- 不要跳过 `todo` 直接开始做事
- `focus` 只维护当前最重要的信息，不要堆历史
- `finish` 不等于 `achieve`
- `reflect realize master` 适合在一次工作闭环后一起使用
- 如果旧规则已经失效，及时用 `forget` 清理，不要继续沿用

## 响应约定

使用 `heroagent` 时，推荐使用单行状态头，例如：

```md
✅ HeroAgent · 计划制定
❓ HeroAgent · 需要确认
⚠️ HeroAgent · 进度聚焦
💡 HeroAgent · 咨询问答
```

不再要求单独输出 `[HeroAgent]`。

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

- `SKILL.md`：skill 主入口
- `references/`：路由、输出规范、文件约定等参考资料
- `assets/templates/`：目标、计划、任务、复盘、原则、流程模板
- `scripts/`：初始化、引导、更新、归档、自检脚本

## 建议阅读顺序

如果你第一次接触这个仓库，建议按这个顺序看：

1. `README.md`
2. `SKILL.md`
3. `scripts/`

## 适用场景

HeroAgent 适合以下类型的工作：

- 需求澄清
- 项目规划
- 长期任务推进
- 团队流程整理
- 工作复盘
- 知识沉淀
- 方法教学
- 规则淘汰与迁移
