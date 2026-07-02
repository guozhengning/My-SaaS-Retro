# SaaS Retro 校园系统 V1.1 数据库表设计

## 1. 设计目标

本文档基于 [docs/api-v1.md](/C:/Users/lenovo/Desktop/SaaS_retro/docs/api-v1.md) 拆解数据库表结构，目标是支撑以下能力：
- 多学校租户隔离
- 学校、班级、学生、教师基础管理
- 可配置流程模板与流程实例
- 可配置评教模板与评教任务
- 课程级成绩方案、考试成绩录入与发布

默认假设：
- 使用关系型数据库，推荐 MySQL 8.x 或 PostgreSQL。
- 主键统一使用 `bigint`。
- 所有核心业务表默认包含 `id`、`created_at`、`updated_at`。
- 涉及学校隔离的业务表默认包含 `school_id`。
- 逻辑删除统一使用 `is_deleted`，默认 `0`。

## 2. 表总览

### 2.1 基础组织
- `schools`
- `users`
- `student_profiles`
- `teacher_profiles`
- `grades`
- `classes`
- `courses`
- `class_students`
- `teacher_courses`
- `timetable_entries`

### 2.2 流程引擎与业务单据
- `workflow_templates`
- `workflow_template_nodes`
- `workflow_instances`
- `workflow_instance_nodes`
- `workflow_tasks`
- `workflow_action_logs`
- `leave_requests`
- `certificate_types`
- `certificate_requests`

### 2.3 评教
- `evaluation_templates`
- `evaluation_dimensions`
- `evaluation_tasks`
- `evaluation_task_targets`
- `evaluation_submissions`
- `evaluation_submission_items`

### 2.4 考试与成绩
- `score_schemes`
- `score_scheme_items`
- `exams`
- `exam_classes`
- `exam_courses`
- `exam_course_score_schemes`
- `student_score_records`
- `student_score_items`

## 3. 基础组织表

### 3.1 `schools`
学校租户主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 学校 ID |
| `name` | varchar(128) | 学校名称 |
| `code` | varchar(64) | 学校编码，全局唯一 |
| `contact_name` | varchar(64) | 联系人 |
| `contact_phone` | varchar(32) | 联系电话 |
| `status` | varchar(16) | `active` / `inactive` |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_schools_code(code)`

### 3.2 `users`
统一账号表，存平台管理员、学校管理员、教师、学生登录账号。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 用户 ID |
| `school_id` | bigint nullable | 平台管理员可为空，学校用户必填 |
| `role` | varchar(32) | `platform_admin` / `school_admin` / `teacher` / `student` |
| `login_id` | varchar(64) | 登录账号，可存学号/工号/手机号 |
| `password_hash` | varchar(255) | 密码哈希 |
| `name` | varchar(64) | 姓名 |
| `phone` | varchar(32) | 手机号 |
| `status` | varchar(16) | `active` / `inactive` |
| `last_login_at` | datetime nullable | 最后登录时间 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_users_role_login(role, login_id, is_deleted)`
- `idx_users_school_role(school_id, role)`

### 3.3 `student_profiles`
学生档案表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 学生档案 ID |
| `school_id` | bigint | 学校 ID |
| `user_id` | bigint | 对应 `users.id` |
| `student_no` | varchar(64) | 学号 |
| `name` | varchar(64) | 学生姓名 |
| `gender` | varchar(16) | 性别 |
| `grade_id` | bigint | 当前年级 |
| `class_id` | bigint | 当前班级 |
| `phone` | varchar(32) | 联系电话 |
| `status` | varchar(16) | `active` / `inactive` |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_student_profiles_school_no(school_id, student_no, is_deleted)`
- `idx_student_profiles_class(class_id)`

### 3.4 `teacher_profiles`
教师档案表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 教师档案 ID |
| `school_id` | bigint | 学校 ID |
| `user_id` | bigint | 对应 `users.id` |
| `employee_no` | varchar(64) | 工号 |
| `name` | varchar(64) | 教师姓名 |
| `phone` | varchar(32) | 手机号 |
| `status` | varchar(16) | 启停用状态 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_teacher_profiles_school_no(school_id, employee_no, is_deleted)`

### 3.5 `grades`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 年级 ID |
| `school_id` | bigint | 学校 ID |
| `name` | varchar(64) | 年级名称 |
| `academic_year` | varchar(32) | 学年 |
| `status` | varchar(16) | 状态 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 3.6 `classes`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 班级 ID |
| `school_id` | bigint | 学校 ID |
| `grade_id` | bigint | 年级 ID |
| `name` | varchar(64) | 班级名称 |
| `head_teacher_id` | bigint nullable | 班主任教师档案 ID |
| `status` | varchar(16) | 状态 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_classes_school_grade_name(school_id, grade_id, name, is_deleted)`

### 3.7 `courses`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 课程 ID |
| `school_id` | bigint | 学校 ID |
| `name` | varchar(128) | 课程名称 |
| `code` | varchar(64) | 课程编码 |
| `credit` | decimal(6,2) | 学分 |
| `status` | varchar(16) | 状态 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_courses_school_code(school_id, code, is_deleted)`

### 3.8 `class_students`
学生与班级关系表。虽然 V1.1 一个学生只有一个当前班级，但独立关系表更容易保留历史。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `class_id` | bigint | 班级 ID |
| `student_id` | bigint | 学生档案 ID |
| `is_current` | tinyint | 是否当前班级 |
| `joined_at` | date | 入班日期 |
| `left_at` | date nullable | 离班日期 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 3.9 `teacher_courses`
教师授课关系表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `teacher_id` | bigint | 教师档案 ID |
| `course_id` | bigint | 课程 ID |
| `class_id` | bigint | 班级 ID |
| `term` | varchar(32) | 学期 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `idx_teacher_courses_teacher_term(teacher_id, term)`
- `idx_teacher_courses_class_course(class_id, course_id, term)`

### 3.10 `timetable_entries`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 课表记录 ID |
| `school_id` | bigint | 学校 ID |
| `term` | varchar(32) | 学期 |
| `class_id` | bigint | 班级 ID |
| `course_id` | bigint | 课程 ID |
| `teacher_id` | bigint | 教师档案 ID |
| `weekday` | tinyint | 星期几 1-7 |
| `period` | tinyint | 第几节 |
| `start_time` | time | 开始时间 |
| `end_time` | time | 结束时间 |
| `location` | varchar(128) | 上课地点 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

## 4. 流程引擎与业务单据

### 4.1 `workflow_templates`
流程模板主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 模板 ID |
| `school_id` | bigint | 学校 ID |
| `workflow_type_key` | varchar(64) | `leave_request` / `certificate_request` |
| `name` | varchar(128) | 模板名称 |
| `status` | varchar(16) | `draft` / `active` / `inactive` |
| `version` | int | 模板版本号 |
| `created_by` | bigint | 创建人用户 ID |
| `updated_by` | bigint | 更新人用户 ID |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `idx_workflow_templates_school_type(school_id, workflow_type_key, status)`

### 4.2 `workflow_template_nodes`
流程模板节点表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 节点 ID |
| `school_id` | bigint | 学校 ID |
| `template_id` | bigint | 流程模板 ID |
| `node_key` | varchar(64) | 节点编码 |
| `node_name` | varchar(64) | 节点名称 |
| `node_type_key` | varchar(32) | `start` / `approval` / `issue` / `end` |
| `approver_type_key` | varchar(32) nullable | 审批人类型 |
| `sort_order` | int | 顺序 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_workflow_template_nodes_template_key(template_id, node_key)`
- `idx_workflow_template_nodes_template_sort(template_id, sort_order)`

### 4.3 `workflow_instances`
业务发起后生成的流程实例主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 流程实例 ID |
| `school_id` | bigint | 学校 ID |
| `workflow_type_key` | varchar(64) | 流程类型 |
| `template_id` | bigint | 使用的流程模板 ID |
| `template_version` | int | 模板版本号快照 |
| `business_type` | varchar(64) | `leave_request` / `certificate_request` |
| `business_id` | bigint | 对应业务单据 ID |
| `current_node_key` | varchar(64) nullable | 当前节点编码 |
| `current_node_name` | varchar(64) nullable | 当前节点名称 |
| `instance_status` | varchar(32) | 流程状态 |
| `started_by` | bigint | 发起人用户 ID |
| `started_at` | datetime | 发起时间 |
| `finished_at` | datetime nullable | 完成时间 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_workflow_instances_business(business_type, business_id)`
- `idx_workflow_instances_school_status(school_id, instance_status)`

### 4.4 `workflow_instance_nodes`
流程实例节点快照表，保存发起时节点结构。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `instance_id` | bigint | 流程实例 ID |
| `node_key` | varchar(64) | 节点编码 |
| `node_name` | varchar(64) | 节点名称 |
| `node_type_key` | varchar(32) | 节点类型 |
| `approver_type_key` | varchar(32) nullable | 审批人类型 |
| `sort_order` | int | 顺序 |
| `node_status` | varchar(32) | 节点状态 |
| `started_at` | datetime nullable | 节点开始时间 |
| `finished_at` | datetime nullable | 节点结束时间 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 4.5 `workflow_tasks`
流程待办表，给教师/学校管理员处理。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 任务 ID |
| `school_id` | bigint | 学校 ID |
| `instance_id` | bigint | 流程实例 ID |
| `business_type` | varchar(64) | 业务类型 |
| `business_id` | bigint | 业务单据 ID |
| `node_key` | varchar(64) | 当前节点编码 |
| `node_name` | varchar(64) | 当前节点名称 |
| `approver_type_key` | varchar(32) | 审批人类型 |
| `assignee_user_id` | bigint nullable | 实际处理人 |
| `task_status` | varchar(32) | 任务状态 |
| `actioned_at` | datetime nullable | 处理时间 |
| `comment` | varchar(255) nullable | 处理意见 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 4.6 `workflow_action_logs`
流程操作日志表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 日志 ID |
| `school_id` | bigint | 学校 ID |
| `instance_id` | bigint | 流程实例 ID |
| `business_type` | varchar(64) | 业务类型 |
| `business_id` | bigint | 业务单据 ID |
| `node_key` | varchar(64) nullable | 操作节点 |
| `action_key` | varchar(32) | `submit` / `approve` / `reject` 等 |
| `operator_user_id` | bigint | 操作人用户 ID |
| `operator_role` | varchar(32) | 操作人角色 |
| `comment` | varchar(255) nullable | 操作意见 |
| `created_at` | datetime | 操作时间 |

### 4.7 `leave_requests`
请假单主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 请假单 ID |
| `school_id` | bigint | 学校 ID |
| `student_id` | bigint | 学生档案 ID |
| `workflow_template_id` | bigint | 流程模板 ID |
| `workflow_instance_id` | bigint nullable | 流程实例 ID |
| `start_at` | datetime | 请假开始时间 |
| `end_at` | datetime | 请假结束时间 |
| `reason` | varchar(255) | 请假原因 |
| `instance_status` | varchar(32) | 当前流程状态 |
| `created_by` | bigint | 发起人用户 ID |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 4.8 `certificate_types`
证明类型表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 证明类型 ID |
| `school_id` | bigint | 学校 ID |
| `name` | varchar(128) | 证明名称 |
| `description` | varchar(255) | 说明 |
| `status` | varchar(16) | `active` / `inactive` |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 4.9 `certificate_requests`
证明申请主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 证明申请 ID |
| `school_id` | bigint | 学校 ID |
| `student_id` | bigint | 学生档案 ID |
| `certificate_type_id` | bigint | 证明类型 ID |
| `workflow_template_id` | bigint | 流程模板 ID |
| `workflow_instance_id` | bigint nullable | 流程实例 ID |
| `purpose` | varchar(255) | 申请用途 |
| `copies` | int | 申请份数 |
| `instance_status` | varchar(32) | 当前流程状态 |
| `download_url` | varchar(255) nullable | 下载地址 |
| `created_by` | bigint | 发起人用户 ID |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

## 5. 评教表

### 5.1 `evaluation_templates`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 模板 ID |
| `school_id` | bigint | 学校 ID |
| `template_key` | varchar(64) | 模板编码 |
| `name` | varchar(128) | 模板名称 |
| `anonymous_mode` | varchar(32) | `anonymous` / `real_name` |
| `score_scale_type` | varchar(32) | 分制类型 |
| `score_min` | decimal(8,2) | 模板最小分 |
| `score_max` | decimal(8,2) | 模板最大分 |
| `status` | varchar(16) | 状态 |
| `created_by` | bigint | 创建人 |
| `updated_by` | bigint | 更新人 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_evaluation_templates_school_key(school_id, template_key, is_deleted)`

### 5.2 `evaluation_dimensions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 维度 ID |
| `school_id` | bigint | 学校 ID |
| `template_id` | bigint | 模板 ID |
| `dimension_key` | varchar(64) | 维度编码 |
| `dimension_name` | varchar(64) | 维度名称 |
| `weight` | decimal(6,2) | 权重 |
| `score_min` | decimal(8,2) | 最小分 |
| `score_max` | decimal(8,2) | 最大分 |
| `required_flag` | tinyint | 是否必填 |
| `comment_enabled` | tinyint | 是否允许文本意见 |
| `sort_order` | int | 排序 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 5.3 `evaluation_tasks`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 任务 ID |
| `school_id` | bigint | 学校 ID |
| `template_id` | bigint | 评教模板 ID |
| `name` | varchar(128) | 任务名称 |
| `target_type` | varchar(32) | 当前先支持 `class` |
| `anonymous_mode` | varchar(32) | 任务匿名模式 |
| `start_at` | datetime | 开始时间 |
| `end_at` | datetime | 结束时间 |
| `status` | varchar(16) | `draft` / `published` / `closed` |
| `created_by` | bigint | 创建人 |
| `updated_by` | bigint | 更新人 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 5.4 `evaluation_task_targets`
评教任务目标范围表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `task_id` | bigint | 任务 ID |
| `target_type` | varchar(32) | `class` |
| `target_id` | bigint | 班级 ID |
| `created_at` | datetime | 创建时间 |

### 5.5 `evaluation_submissions`
评教提交主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 提交 ID |
| `school_id` | bigint | 学校 ID |
| `task_id` | bigint | 评教任务 ID |
| `student_id` | bigint | 学生档案 ID |
| `teacher_id` | bigint | 教师档案 ID |
| `course_id` | bigint | 课程 ID |
| `weighted_score` | decimal(8,2) | 加权总分 |
| `submitted_at` | datetime | 提交时间 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_evaluation_submissions_unique(task_id, student_id, teacher_id, course_id)`

### 5.6 `evaluation_submission_items`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `submission_id` | bigint | 提交 ID |
| `dimension_id` | bigint | 模板维度 ID |
| `dimension_key` | varchar(64) | 维度编码快照 |
| `dimension_name` | varchar(64) | 维度名称快照 |
| `weight` | decimal(6,2) | 权重快照 |
| `raw_score` | decimal(8,2) nullable | 原始分值 |
| `comment` | text nullable | 文本意见 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

## 6. 考试与成绩表

### 6.1 `score_schemes`
课程级成绩方案主表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 方案 ID |
| `school_id` | bigint | 学校 ID |
| `course_id` | bigint | 课程 ID |
| `scheme_name` | varchar(128) | 方案名称 |
| `status` | varchar(16) | `active` / `inactive` |
| `version` | int | 方案版本号 |
| `created_by` | bigint | 创建人 |
| `updated_by` | bigint | 更新人 |
| `is_deleted` | tinyint | 逻辑删除 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 6.2 `score_scheme_items`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 成绩项 ID |
| `school_id` | bigint | 学校 ID |
| `scheme_id` | bigint | 成绩方案 ID |
| `item_key` | varchar(64) | 成绩项编码 |
| `item_name` | varchar(64) | 成绩项名称 |
| `weight` | decimal(6,2) | 权重 |
| `score_type` | varchar(32) | `numeric` / `grade` / `pass_fail` |
| `score_min` | decimal(8,2) nullable | 最小分 |
| `score_max` | decimal(8,2) nullable | 最大分 |
| `decimal_places` | tinyint | 小数位数 |
| `is_required` | tinyint | 是否必填 |
| `counts_in_final` | tinyint | 是否计入总评 |
| `allows_makeup` | tinyint | 是否允许补考 |
| `sort_order` | int | 排序 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_score_scheme_items_scheme_key(scheme_id, item_key)`

### 6.3 `exams`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 考试 ID |
| `school_id` | bigint | 学校 ID |
| `name` | varchar(128) | 考试名称 |
| `term` | varchar(32) | 学期 |
| `start_date` | date | 开始日期 |
| `end_date` | date | 结束日期 |
| `status` | varchar(16) | `draft` / `published` / `closed` |
| `created_by` | bigint | 创建人 |
| `updated_by` | bigint | 更新人 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 6.4 `exam_classes`
考试关联班级表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `exam_id` | bigint | 考试 ID |
| `class_id` | bigint | 班级 ID |
| `created_at` | datetime | 创建时间 |

### 6.5 `exam_courses`
考试关联课程表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `exam_id` | bigint | 考试 ID |
| `course_id` | bigint | 课程 ID |
| `score_scheme_id` | bigint | 原方案 ID |
| `created_at` | datetime | 创建时间 |

### 6.6 `exam_course_score_schemes`
考试课程成绩方案快照表。考试发布或创建时生成。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `exam_id` | bigint | 考试 ID |
| `course_id` | bigint | 课程 ID |
| `source_scheme_id` | bigint | 来源成绩方案 ID |
| `source_scheme_version` | int | 来源方案版本 |
| `scheme_name` | varchar(128) | 方案名称快照 |
| `status` | varchar(16) | 快照状态 |
| `snapshot_json` | json / text | 整套方案快照 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_exam_course_score_schemes_exam_course(exam_id, course_id)`

### 6.7 `student_score_records`
学生成绩主记录表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 成绩记录 ID |
| `school_id` | bigint | 学校 ID |
| `exam_id` | bigint | 考试 ID |
| `class_id` | bigint | 班级 ID |
| `student_id` | bigint | 学生档案 ID |
| `course_id` | bigint | 课程 ID |
| `scheme_snapshot_id` | bigint | 对应 `exam_course_score_schemes.id` |
| `raw_total_score` | decimal(8,2) nullable | 原始累计分 |
| `final_score` | decimal(8,2) nullable | 总评分 |
| `grade_level` | varchar(32) nullable | 等级 |
| `grade_point` | decimal(6,2) nullable | 绩点 |
| `publish_status` | varchar(16) | `draft` / `published` / `hidden` |
| `published_at` | datetime nullable | 发布时间 |
| `is_absent` | tinyint | 是否缺考 |
| `is_cheating` | tinyint | 是否作弊 |
| `is_makeup` | tinyint | 是否补考 |
| `remark` | varchar(255) nullable | 备注 |
| `created_by` | bigint | 录入人 |
| `updated_by` | bigint | 更新人 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

索引建议：
- `uk_student_score_records_exam_student_course(exam_id, student_id, course_id)`
- `idx_student_score_records_student(student_id, publish_status)`

### 6.8 `student_score_items`
学生成绩分项明细表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | bigint PK | 主键 |
| `school_id` | bigint | 学校 ID |
| `score_record_id` | bigint | 成绩主记录 ID |
| `item_key` | varchar(64) | 成绩项编码快照 |
| `item_name` | varchar(64) | 成绩项名称快照 |
| `weight` | decimal(6,2) | 权重快照 |
| `score_type` | varchar(32) | 成绩项类型 |
| `score_value` | decimal(8,2) nullable | 数值分 |
| `grade_value` | varchar(32) nullable | 等级值 |
| `pass_flag` | tinyint nullable | 合格标记 |
| `counts_in_final` | tinyint | 是否计入总评 |
| `remark` | varchar(255) nullable | 备注 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

## 7. 关键外键关系

建议在数据库中建立以下核心外键或至少以应用层保证一致性：
- `student_profiles.user_id -> users.id`
- `teacher_profiles.user_id -> users.id`
- `classes.grade_id -> grades.id`
- `student_profiles.class_id -> classes.id`
- `student_profiles.grade_id -> grades.id`
- `workflow_template_nodes.template_id -> workflow_templates.id`
- `workflow_instances.template_id -> workflow_templates.id`
- `workflow_tasks.instance_id -> workflow_instances.id`
- `leave_requests.workflow_instance_id -> workflow_instances.id`
- `certificate_requests.workflow_instance_id -> workflow_instances.id`
- `evaluation_dimensions.template_id -> evaluation_templates.id`
- `evaluation_tasks.template_id -> evaluation_templates.id`
- `evaluation_submissions.task_id -> evaluation_tasks.id`
- `score_scheme_items.scheme_id -> score_schemes.id`
- `exam_course_score_schemes.exam_id -> exams.id`
- `student_score_records.scheme_snapshot_id -> exam_course_score_schemes.id`
- `student_score_items.score_record_id -> student_score_records.id`

## 8. 接口与数据表映射

### 8.1 流程模板接口
- `POST /workflow-templates`
  - 写入 `workflow_templates`
  - 批量写入 `workflow_template_nodes`
- `POST /workflow-templates/{template_id}/activate`
  - 更新 `workflow_templates.status`

### 8.2 请假与证明接口
- `POST /leave-requests`
  - 写入 `leave_requests`
  - 创建 `workflow_instances`
  - 生成 `workflow_instance_nodes`
  - 创建首个 `workflow_tasks`
  - 写入 `workflow_action_logs`
- `POST /certificate-requests`
  - 写入 `certificate_requests`
  - 其余流程表同上
- `POST /leave-requests/{id}/actions`
- `POST /certificate-requests/{id}/actions`
  - 更新 `workflow_tasks`
  - 推进 `workflow_instances`
  - 追加 `workflow_action_logs`
  - 回写 `leave_requests.instance_status` 或 `certificate_requests.instance_status`

### 8.3 评教接口
- `POST /evaluations/templates`
  - 写入 `evaluation_templates`
  - 批量写入 `evaluation_dimensions`
- `POST /evaluations/tasks`
  - 写入 `evaluation_tasks`
  - 批量写入 `evaluation_task_targets`
- `POST /evaluations/tasks/{task_id}/submissions`
  - 写入 `evaluation_submissions`
  - 批量写入 `evaluation_submission_items`

### 8.4 成绩方案与成绩接口
- `POST /score-schemes`
  - 写入 `score_schemes`
  - 批量写入 `score_scheme_items`
- `POST /exams`
  - 写入 `exams`
  - 写入 `exam_classes`
  - 写入 `exam_courses`
  - 生成 `exam_course_score_schemes`
- `POST /exams/{exam_id}/scores:batch-save`
  - upsert `student_score_records`
  - 批量 upsert `student_score_items`
- `POST /exams/{exam_id}/scores/publish`
  - 更新 `student_score_records.publish_status`
  - 更新 `student_score_records.published_at`

## 9. 建表顺序建议

1. `schools`
2. `users`
3. `grades`、`classes`、`courses`
4. `student_profiles`、`teacher_profiles`
5. `class_students`、`teacher_courses`、`timetable_entries`
6. `workflow_templates`、`workflow_template_nodes`
7. `leave_requests`、`certificate_types`、`certificate_requests`
8. `workflow_instances`、`workflow_instance_nodes`、`workflow_tasks`、`workflow_action_logs`
9. `evaluation_templates`、`evaluation_dimensions`
10. `evaluation_tasks`、`evaluation_task_targets`
11. `evaluation_submissions`、`evaluation_submission_items`
12. `score_schemes`、`score_scheme_items`
13. `exams`、`exam_classes`、`exam_courses`、`exam_course_score_schemes`
14. `student_score_records`、`student_score_items`

## 10. 下一步建议

1. 将本文档继续细化为正式 SQL DDL。
2. 明确每张表的字段长度、默认值、非空约束。
3. 补充枚举字典表，或在应用层固化枚举。
4. 决定是否统一引入 `tenant_id`、`created_by`、`updated_by` 基类字段模板。
