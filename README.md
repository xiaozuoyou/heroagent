# HeroAgent

HeroAgent 是一个面向目标推进与认知沉淀的工作流智能体 skill。

它把日常工作拆成两条闭环：

- 推进闭环：`want -> plan -> todo -> focus -> finish -> achieve | abandon`
- 沉淀闭环：`reflect -> realize -> master -> synthesize -> forget`

适合用于目标定义、阶段规划、任务拆解、进度聚焦、复盘总结、原则沉淀、流程固化，以及长期工作流的持续落盘。

## 安装

推荐使用 `npx skills add` 安装。

### 全局安装

```bash
npx skills add xiaozuoyou/heroagent -g -y
```

适合希望在多个项目里复用 `heroagent` 的场景。

### 项目级安装

```bash
npx skills add xiaozuoyou/heroagent -y
```

适合只在当前项目里使用 `heroagent`。

### 安装后检查

```bash
npx skills list -g
```

或在项目中执行：

```bash
npx skills list
```

如果需要更新，重新执行一次安装命令即可。

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

### 附带脚本

仓库内已经提供一组可执行脚本：

- `scripts/init_heroagent.py`：初始化 `.heroagent/`
- `scripts/bootstrap_first_goal.py`：生成首批目标、计划、任务草稿
- `scripts/update_current_focus.py`：更新 `current-focus.md`
- `scripts/archive_goal.py`：归档已完成或已放弃目标
- `scripts/doctor_heroagent.py`：检查工作区是否健康

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

使用 `heroagent` 时，回复第一行必须是：

```md
[HeroAgent]
```

这是这个 skill 的固定输出约束。

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
- `references/`：路由、输出契约、文件约定、运行手册等参考资料
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
