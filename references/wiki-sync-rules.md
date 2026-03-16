# Wiki 同步规则

## 使用规则

代码或项目结构发生变化时，按这里决定 wiki 检查和同步。

## 同步原则

- 先消费现有 wiki，再判断是否需要补写
- 以代码事实为准，不以历史 wiki 为准
- 先生成最小更新建议，再决定是否直接写入
- 一次变更可以命中多个 wiki 文件
- 高频做 `detect`，低频做 `sync`

## 同步判断顺序

1. 先识别本次变更是否已直接修改 `.heroagent/wiki/`
2. 若未直接修改 wiki，再根据变更路径推导建议更新的 wiki 文件
3. 若建议结果为空，只在确有知识变化时再人工补充
4. 若暂不直接写正文，先在 `wiki/drafts/` 生成待补写草稿
5. 草稿确认后，合并回正式 wiki
6. 更新正文后，刷新 `wiki/index.md` 与 `wiki/registry.json`
7. 定期输出维护报告，检查缺失草稿与陈旧草稿
8. 按策略自动收敛可自动处理的维护项
9. 定期压缩正式 wiki 的重复自动补充块
10. 用信号评分重新排序维护优先级
11. 在具体动作执行前装配对应上下文包
12. 优先从代码变更中提炼稳定事实，再回写 wiki
13. 由维护策略决定自动化强度

## `detect` 与 `sync`

把 wiki 处理拆成两步：

1. `detect`：只判断本轮变更是否会让 wiki 失真，并记录待同步目标
2. `sync`：在关键节点再真正补写、生成草稿或合并正式 wiki

执行规则：

- 默认在执行 `todo` 之后、已经产生实际代码变更时，再做 `detect`
- `want`、`plan`、`todo` 阶段通常只改工作流状态
- 若讨论阶段已经明确改写了需求边界、架构约束、接口契约或数据模型，可例外补一次 `detect`
- 进入 `achieve` 或显式 `wiki` 请求前，优先补一次正式同步判断
- 若只生成草稿，正式 wiki 仍视为未同步完成
- `detect` 由 skill 在内部自动执行

## 文件映射规则

### `overview.md`

优先在以下变更后检查：

- 项目入口说明变更
- `README.md`、`package.json`、`pyproject.toml` 等项目级文件变更
- 文档目录或工作流目录变更
- 项目目标、模块总览、当前重点发生变化

### `arch.md`

优先在以下变更后检查：

- 部署、基础设施、容器、配置结构变更
- `Dockerfile`、`docker-compose.*`、`infra/`、`config/` 等文件变更
- 核心模块关系或技术约束发生变化

### `api.md`

优先在以下变更后检查：

- 路由、控制器、接口协议、对外契约变更
- `api/`、`routes/`、`controllers/`、`graphql/` 等路径变更
- 接口入参与出参约定变化

### `data.md`

优先在以下变更后检查：

- 数据模型、数据库结构、迁移文件变更
- `models/`、`schemas/`、`migrations/`、`prisma/`、`*.sql` 等路径变更
- 核心实体、字段约束、数据流发生变化

### `modules/*.md`

优先在以下变更后检查：

- 业务模块目录下的实现文件变更
- `src/<module>/`、`app/<module>/`、`services/<module>/`、`packages/<module>/` 等路径变更
- 某一模块职责、依赖、边界发生变化

## 最小自动建议

可直接使用：

```bash
python3 scripts/suggest_wiki_updates.py <changed-path>...
```

示例：

```bash
python3 scripts/suggest_wiki_updates.py \
  src/payments/service.ts \
  src/api/routes/orders.ts \
  prisma/schema.prisma
```

期望输出：

- `api.md`
- `data.md`
- `modules/payments.md`

## 人工补位

以下情况不要只依赖路径映射：

- 同一路径下发生的是重构而非知识变化
- 文案修改没有改变项目事实
- 小范围修 bug 不影响架构、接口、数据或模块边界

这时先回答两个问题：

- 这次变更是否改变了别人理解项目所需的事实
- 如果新成员只读当前 wiki，会不会得到过时结论

只要其中一个答案是“会”，就应更新对应 wiki。
