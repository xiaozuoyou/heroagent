# 运行手册参考

## 目的

给 `heroagent` 一套最小可执行的日常使用顺序，避免用户只看到脚本列表却不知道如何串起来。

## 标准使用顺序

### 1. 初始化工作区

在目标项目中创建 `.heroagent/` 基础结构：

```bash
python3 scripts/init_heroagent.py /path/to/project
```

### 2. 生成首批目标文件

根据一个目标标题生成第一批工作文件：

```bash
python3 scripts/bootstrap_first_goal.py "规范团队周报流程" /path/to/project --refresh-focus
```

### 3. 推进过程中更新当前焦点

当目标、阶段、阻塞、下一步发生变化时，更新 `current-focus.md`：

```bash
python3 scripts/update_current_focus.py \
  --goal "规范团队周报流程" \
  --stage focus \
  --completed "已产出首批目标、计划、任务草稿" \
  --in-progress "补全目标边界与阶段计划" \
  --blockers "无" \
  --next-step "先明确周报成功标准" \
  /path/to/project
```

### 4. 目标完成或放弃后归档

```bash
python3 scripts/archive_goal.py --slug goal-d348d219 --reset-focus /path/to/project
```

### 5. 发现问题时执行健康检查

```bash
python3 scripts/doctor_heroagent.py /path/to/project
```

## 典型节奏

适合长期目标的最小循环：

1. `want`：生成或补全目标卡片
2. `plan`：补齐阶段计划
3. `todo`：落成任务清单
4. `focus`：维护 `current-focus.md`
5. `finish`：根据任务完成情况更新状态
6. `achieve` 或 `abandon`：收口后归档

## 常见问题

### 只想讨论，不想落盘

可以只使用 `heroagent` 的动作规则，不运行脚本。

### 已有 `.heroagent/`

脚本默认补缺，不覆盖现有内容；需要特别刷新时，再显式使用对应参数。

### 不知道 `slug`

优先从 `goals/`、`plans/`、`tasks/` 文件名中查看；中文标题回退时会生成 `goal-xxxxxxxx` 形式的安全 `slug`。
