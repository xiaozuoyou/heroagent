# Wiki 约定参考

## 目的

定义 `.heroagent/wiki/` 的目录结构、维护方式和消费时机。

## 执行原则

- 把 wiki 作为优先上下文来源
- 能从 wiki 获取的项目信息，优先不再向用户重复追问
- wiki 与代码冲突时，以代码事实为准，并更新 wiki

## 目录结构

```text
.heroagent/wiki/
├── index.md
├── registry.json
├── drafts/
├── overview.md
├── arch.md
├── api.md
├── data.md
└── modules/
```

## 文件职责

- `index.md`：AI 优先阅读的索引与状态摘要
- `registry.json`：供 AI 或脚本消费的结构化元信息
- `drafts/`：根据代码变更自动生成的待补写草稿
- `overview.md`：项目目标、模块总览、当前重点
- `arch.md`：架构设计、模块关系、技术约束
- `api.md`：对外接口、集成边界、调用约定
- `data.md`：核心实体、字段约束、数据流
- `modules/*.md`：模块级补充知识

模块级 wiki 按单模块单文件维护，例如：

- `modules/payments.md`
- `modules/auth.md`
- `modules/reporting.md`

## 消费时机

在以下场景，优先读取 `.heroagent/wiki/`：

- `want` 前需要确认已有项目目标、边界、约束
- `plan` 前需要确认模块结构、架构依赖
- `todo` 前需要定位相关模块
- `focus` 前需要补齐当前背景
- `reflect` 时需要结合历史架构或数据背景判断根因

## 更新时机

在以下场景，触发 wiki 更新判断：

- 初始化工作区后，开始接管老项目
- 对现有模块形成了更清晰认知
- API、数据模型、架构边界发生变化
- 用户明确要求维护知识库

若已知本轮变更路径，先参考 `references/wiki-sync-rules.md` 推导应更新的 wiki 文件，再做最小改动。

若本轮先不改正文，先在 `wiki/drafts/` 生成草稿，再合并回正式 wiki。

执行闭环：

1. 根据变更生成 `drafts/`
2. AI 审阅并补强草稿
3. 把确认后的草稿合并进正式 wiki
4. 刷新 `index.md` 与 `registry.json`
5. 定期生成维护报告，检查缺失草稿与陈旧草稿
6. 按策略自动收敛维护债务
7. 定期压缩正式 wiki 的重复补充块
8. 通过信号评分决定维护优先级与上下文优先级
9. 按动作装配最小可用上下文包
10. 从代码变更中提炼更稳定的事实线索
11. 用显式策略控制自动维护强度

## 消费顺序

按以下顺序：

1. 先读 `wiki/index.md` 或 `wiki/registry.json`
2. 再读 `.heroagent/wiki/` 中被索引标记为最相关的文件
3. wiki 不足，再读 `.heroagent/progress/`、`goals/`、`plans/`
4. 仍不足，再扫描代码或继续追问用户

只有 wiki 不足时，再继续扫描代码。
