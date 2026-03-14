# Wiki 约定参考

## 目的

定义 `.heroagent/wiki/` 的目录结构、维护方式，以及 HeroAgent 在何时应消费这些知识作为上下文。

## 核心原则

- wiki 不只是存储区，也是优先上下文来源
- 能从 wiki 获取的项目信息，优先不再向用户重复追问
- wiki 与代码冲突时，以代码事实为准，并更新 wiki

## 目录结构

```text
.heroagent/wiki/
├── overview.md
├── arch.md
├── api.md
├── data.md
└── modules/
```

## 文件职责

- `overview.md`：项目目标、模块总览、当前重点
- `arch.md`：架构设计、模块关系、技术约束
- `api.md`：对外接口、集成边界、调用约定
- `data.md`：核心实体、字段约束、数据流
- `modules/*.md`：模块级补充知识

## 何时优先消费 wiki

在以下场景，优先读取 `.heroagent/wiki/`：

- `want` 前需要确认已有项目目标、边界、约束
- `plan` 前需要确认模块结构、架构依赖
- `todo` 前需要定位相关模块
- `focus` 前需要补齐当前背景
- `reflect` 时需要结合历史架构或数据背景判断根因

## 何时更新 wiki

在以下场景，应考虑更新 wiki：

- 初始化工作区后，开始接管老项目
- 对现有模块形成了更清晰认知
- API、数据模型、架构边界发生变化
- 用户明确要求维护知识库

## 消费顺序

默认顺序：

1. 先读 `.heroagent/wiki/`
2. wiki 不足，再读 `.heroagent/progress/`、`goals/`、`plans/`
3. 仍不足，再扫描代码或继续追问用户

不要跳过 wiki 直接扫描代码。
