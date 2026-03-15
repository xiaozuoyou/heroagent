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

## 对话使用

正常使用 `heroagent` 时，你主要通过自然语言或 `~动作` 触发，底层脚本应由 skill 自动选择和执行，而不是让你手动敲命令。

### 示例一

你可以这样说：

- `在这个老项目里初始化 heroagent`
- `~init`

预期结果：

- 自动创建 `.heroagent/`
- 自动补齐 `goals plans tasks progress wiki` 等目录
- 若适合长期推进，再继续进入 `want`、`plan` 或 `todo`

### 示例二

你可以这样说：

- `帮我更新这个项目的 wiki`
- `把支付模块的知识补到 wiki`
- `~wiki`

预期结果：

- 自动判断应更新 `overview arch api data modules` 中的哪些文件
- 必要时自动生成草稿、刷新索引和注册表
- 若你给出的信息已经够明确，会直接写回正式 wiki

### 示例三

你可以这样说：

- `我刚改了支付模块、订单路由和 prisma，帮我同步 wiki`
- `根据这些变更整理知识库`

预期结果：

- 自动推导应同步哪些 wiki
- 自动生成待补写草稿
- 自动提炼一部分更稳定的源码事实
- 根据当前策略决定是否直接合并、是否压缩旧补充块

### 示例四

你可以这样说：

- `现在最值得先维护哪些 wiki`
- `给我装配 todo 需要的上下文`
- `帮我检查一下 wiki 维护债务`

预期结果：

- 自动给 wiki 打信号分并排序
- 自动挑选当前动作最适合的上下文包
- 自动输出缺失草稿、陈旧草稿、可合并草稿等维护结论

### 示例五

你可以这样说：

- `用保守模式处理这轮 wiki`
- `用平衡策略跑一轮知识库维护`
- `用激进策略把 wiki 自动收口`

预期结果：

- `conservative`：只刷新状态和索引，不主动高侵入更新
- `balanced`：补草稿、标记陈旧、提炼事实，但不自动合并正式 wiki
- `aggressive`：补草稿、合并正文、提炼事实、压缩噪音一起执行

## 常用案例

### 老项目接管

你可以这样说：

- `帮我接管这个老项目，先初始化 heroagent`

典型结果：

- 自动创建 `.heroagent/`
- 自动补齐基础目录和 wiki
- 自动把后续动作收敛到 `want` 或 `plan`

### 新需求启动

你可以这样说：

- `我想把订单退款流程规范起来，先帮我定目标`
- `~want`

典型结果：

- 先做目标完整度评分
- 若信息不足，进入目标澄清
- 若信息足够，输出正式目标卡片

### 目标拆计划

你可以这样说：

- `目标已经明确了，帮我拆一个两周计划`
- `~plan`

典型结果：

- 输出阶段路径
- 标出关键依赖与风险
- 给出每个阶段的完成标志

### 计划拆任务

你可以这样说：

- `把这个计划拆成可执行 todo`
- `~todo`

典型结果：

- 输出动作化任务清单
- 每项任务带完成定义和依赖
- 优先结合模块、API、数据约束来拆解

### 当前进度聚焦

你可以这样说：

- `我现在最该盯什么`
- `~focus`

典型结果：

- 汇总当前目标、阶段、阻塞、下一步
- 优先消费 `wiki` 和 `current-focus.md`
- 不重复无关历史

### 代码变更同步知识库

你可以这样说：

- `我刚改了支付模块和订单接口，帮我同步 wiki`
- `根据这轮改动更新知识库`

典型结果：

- 自动识别应更新哪些 wiki
- 自动生成待补写草稿
- 必要时补充源码事实草稿

### 知识库巡检

你可以这样说：

- `帮我检查一下 wiki 现在的维护状态`
- `看看哪些知识已经陈旧`

典型结果：

- 输出缺失草稿、陈旧草稿、可合并草稿
- 说明当前最值得优先维护的文档
- 必要时建议采用保守、平衡或激进策略

### 任务收口与验收

你可以这样说：

- `这个任务做完了，帮我更新状态`
- `现在算达成了吗`
- `~finish`
- `~achieve`

典型结果：

- `finish` 更新任务完成证据和推进影响
- `achieve` 从目标层面判断是否真正闭环

### 问题复盘与沉淀

你可以这样说：

- `这次延期为什么发生，帮我复盘`
- `把这次经验提炼成原则`
- `把这套方法沉淀成流程`

典型结果：

- `reflect` 拆现象、影响、根因
- `realize` 提炼可迁移原则
- `master` 固化稳定流程

## 手动调试

上面的动作本来应该由 skill 自动触发。  
只有在你要调试、批处理、验证单个能力时，才建议直接运行 `scripts/*.py`。

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
