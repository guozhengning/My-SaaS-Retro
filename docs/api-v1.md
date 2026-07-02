# SaaS Retro 校园系统 V1.1 需求与接口文档

## 1. 产品概述

### 1.1 产品目标
建设一个自用的校园 SaaS 系统，支持在一个平台内管理多所学校的学生业务，并允许学校管理员按本校规则配置流程、评教与成绩方案。

### 1.2 V1.1 版本范围
V1.1 覆盖以下核心模块：
- 认证与账号管理
- 学校与组织管理
- 学生管理
- 课程与课表管理
- 学生评教规则配置与评教任务
- 考试管理
- 成绩方案与成绩管理
- 请假流程配置与请假管理
- 证明流程配置与证明申请管理

### 1.3 多学校租户模型
- 平台服务多所学校。
- 每所学校在业务上视为一个逻辑租户。
- 学校间数据通过 `school_id` 进行隔离。
- 平台管理员可以查看所有学校数据。
- 学校管理员、教师、学生只能访问本校数据。

## 2. 角色与权限

| 角色 | 说明 | 主要权限 |
| --- | --- | --- |
| `platform_admin` | 平台管理员 | 管理学校、创建学校管理员、查看全平台数据 |
| `school_admin` | 学校管理员 | 管理本校学生、班级、课程、考试、流程模板、评教模板、成绩方案 |
| `teacher` | 教师 | 查看授课课表、录入成绩、发布成绩、处理流程待办、查看评教汇总 |
| `student` | 学生 | 查看个人课表、提交评教、查看考试与成绩、提交请假与证明申请 |

## 3. 业务边界与前置假设

### 3.1 本期纳入范围
- 学生使用学号和密码登录
- 教师/管理员使用工号或手机号和密码登录
- 按学生、教师、班级维度查询课表
- 学校可配置请假与证明申请流程模板
- 学校可配置评教维度、权重、分制和匿名模式
- 学校可按课程配置成绩方案与成绩项
- 学校创建考试并绑定成绩方案，由教师录入并发布成绩

### 3.2 本期不纳入范围
- 家长端
- 套餐、计费、订阅管理
- 条件分支审批流、加签、转办、抄送
- 身份证照片、实名核验等高敏感证件能力
- 通知中心、消息推送
- 附件存储中心
- 操作审计日志
- 通用公式引擎

## 4. 核心领域模型

### 4.1 核心对象

| 对象 | 说明 |
| --- | --- |
| `School` | 学校租户 |
| `Grade` | 年级 |
| `Classroom` | 班级 |
| `User` | 通用账号对象 |
| `StudentProfile` | 学生档案 |
| `TeacherProfile` | 教师档案 |
| `Course` | 课程定义 |
| `TimetableEntry` | 课表排课记录 |
| `WorkflowTemplate` | 流程模板 |
| `WorkflowNode` | 流程节点定义 |
| `WorkflowInstance` | 流程实例 |
| `WorkflowTask` | 流程待办 |
| `WorkflowActionLog` | 流程操作记录 |
| `EvaluationTemplate` | 评教模板 |
| `EvaluationDimension` | 评教维度 |
| `EvaluationTask` | 评教任务 |
| `EvaluationSubmission` | 评教提交记录 |
| `Exam` | 考试 |
| `ScoreScheme` | 成绩方案 |
| `ScoreSchemeItem` | 成绩项定义 |
| `ExamCourseScoreScheme` | 考试绑定的课程成绩方案快照 |
| `StudentScoreRecord` | 学生成绩主记录 |
| `StudentScoreItem` | 学生成绩分项记录 |
| `CertificateType` | 证明类型 |
| `CertificateRequest` | 证明申请记录 |
| `LeaveRequest` | 请假申请 |

### 4.2 关系规则
- 一个 `School` 下包含多个年级、班级、课程、教师、学生。
- V1.1 中一个学生只属于一个当前学校和一个当前班级。
- 一条课表记录只属于一个学校、一个学期、一个班级、一个课程、一个教师。
- 一个 `WorkflowTemplate` 只在一个学校内生效，并通过 `workflow_type_key` 区分业务类型。
- 一个请假申请或证明申请在发起时都要绑定一个流程模板，并生成独立的流程实例快照。
- 一个评教模板只在一个学校内生效，可包含多个维度、权重和分制规则。
- 一个评教任务绑定一个评教模板，可面向多个班级或指定目标对象。
- 一个课程可配置多套成绩方案，但同一考试下的同一课程只绑定一套方案快照。
- 一条学生成绩主记录只对应一个考试、一个学生、一个课程；其下可包含多个成绩分项。

## 5. 接口通用约定

### 5.1 基础路径
`/api/v1`

### 5.2 认证方式
- 登录成功后返回访问令牌。
- 后续请求通过 `Authorization: Bearer <token>` 传递令牌。
- Token 中至少包含以下信息：
  - `user_id`
  - `school_id`
  - `role`

### 5.3 通用请求头

```http
Content-Type: application/json
Authorization: Bearer <token>
```

### 5.4 通用响应结构

```json
{
  "code": 0,
  "message": "成功",
  "data": {}
}
```

### 5.5 分页响应结构

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 120
  }
}
```

### 5.6 通用错误码

| 错误码 | 含义 |
| --- | --- |
| `0` | 成功 |
| `40001` | 请求参数错误 |
| `40101` | 认证失败 |
| `40301` | 无权限访问 |
| `40401` | 资源不存在 |
| `40901` | 状态冲突 |
| `42201` | 业务校验失败 |

### 5.7 通用查询参数

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `page` | integer | 页码，默认 `1` |
| `page_size` | integer | 每页条数，默认 `20` |
| `keyword` | string | 模糊搜索关键字 |
| `status` | string | 状态筛选 |

### 5.8 时间格式
- `date`：`YYYY-MM-DD`
- `datetime`：ISO 8601 字符串

## 6. 流程关键字、状态与枚举

### 6.1 用户状态
- `active`：启用
- `inactive`：停用

### 6.2 流程类型关键字 `workflow_type_key`
- `leave_request`：请假申请
- `certificate_request`：证明申请

### 6.3 节点类型关键字 `node_type_key`
- `start`：开始节点
- `approval`：审批节点
- `issue`：出具节点
- `end`：结束节点

### 6.4 审批人类型关键字 `approver_type_key`
- `head_teacher`：班主任
- `course_teacher`：任课教师
- `school_admin`：学校管理员
- `certificate_admin`：证明管理员

### 6.5 动作关键字 `action_key`
- `submit`：提交
- `approve`：通过
- `reject`：拒绝
- `revoke`：撤回
- `resubmit`：重新提交
- `issue`：出具

### 6.6 流程模板状态 `template_status`
- `draft`：草稿
- `active`：启用
- `inactive`：停用

### 6.7 流程实例状态 `instance_status`
- `pending`：待开始
- `in_progress`：处理中
- `approved`：审批通过
- `rejected`：已拒绝
- `revoked`：已撤回
- `issued`：已出具
- `completed`：已完成

### 6.8 流程任务状态 `task_status`
- `pending`：待处理
- `approved`：已通过
- `rejected`：已拒绝
- `revoked`：已撤回
- `issued`：已出具

### 6.9 评教任务状态
- `draft`：草稿
- `published`：已发布
- `closed`：已结束

### 6.10 评教匿名模式 `anonymous_mode`
- `anonymous`：匿名
- `real_name`：实名

### 6.11 评教分制 `score_scale_type`
- `five_point`：5 分制
- `ten_point`：10 分制
- `hundred_point`：100 分制
- `custom`：自定义分制

### 6.12 成绩项类型 `score_type`
- `numeric`：数值分
- `grade`：等级
- `pass_fail`：合格/不合格

### 6.13 成绩发布状态 `publish_status`
- `draft`：草稿
- `published`：已发布
- `hidden`：隐藏

### 6.14 考试状态
- `draft`：草稿
- `published`：已发布
- `closed`：已结束

## 7. 权限矩阵

| 模块 | 平台管理员 | 学校管理员 | 教师 | 学生 |
| --- | --- | --- | --- | --- |
| 学校管理 | 读写 | 无 | 无 | 无 |
| 年级/班级管理 | 只读 | 读写本校 | 只读 | 只读本人相关 |
| 学生管理 | 查看全部 | 读写本校 | 查看所带班级 | 查看本人 |
| 课程管理 | 只读 | 读写本校 | 只读 | 只读本人相关 |
| 课表管理 | 查看全部 | 读写本校 | 查看本人 | 查看本人 |
| 流程模板配置 | 查看全部 | 读写本校 | 只读 | 无 |
| 请假流程实例 | 查看全部 | 查看和处理本校 | 处理负责范围 | 提交和查看本人 |
| 证明流程实例 | 查看全部 | 查看和处理本校 | 处理负责范围 | 提交和查看本人 |
| 评教模板与任务 | 查看全部 | 读写本校 | 查看汇总 | 提交本人 |
| 成绩方案配置 | 查看全部 | 读写本校 | 查看授课课程 | 无 |
| 考试管理 | 查看全部 | 读写本校 | 查看相关班级 | 查看本人 |
| 成绩录入与发布 | 查看全部 | 管理本校 | 录入和发布授课范围 | 查看本人已发布成绩 |

## 8. 接口列表

---

## 8.1 认证与账号

### 8.1.1 登录
- `POST /auth/login`
- 权限：公开接口

请求示例：

```json
{
  "login_id": "20230001",
  "password": "plain-or-hashed-password"
}
```

响应示例：

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "access_token": "jwt-token",
    "token_type": "Bearer",
    "expires_in": 7200,
    "user": {
      "user_id": 1001,
      "school_id": 2001,
      "role": "student",
      "name": "张三"
    }
  }
}
```

### 8.1.2 获取当前登录用户
- `GET /auth/me`
- 权限：登录用户

### 8.1.3 修改密码
- `POST /auth/change-password`
- 权限：登录用户

### 8.1.4 退出登录
- `POST /auth/logout`
- 权限：登录用户

---

## 8.2 学校与组织管理

### 8.2.1 创建学校
- `POST /schools`
- 权限：`platform_admin`

### 8.2.2 学校列表
- `GET /schools`
- 权限：`platform_admin`

### 8.2.3 学校详情
- `GET /schools/{school_id}`
- 权限：`platform_admin`、`school_admin`

### 8.2.4 创建学校管理员
- `POST /schools/{school_id}/admins`
- 权限：`platform_admin`

### 8.2.5 创建年级
- `POST /schools/{school_id}/grades`
- 权限：`school_admin`

### 8.2.6 创建班级
- `POST /schools/{school_id}/classes`
- 权限：`school_admin`

### 8.2.7 班级列表
- `GET /schools/{school_id}/classes`
- 权限：`school_admin`、`teacher`

---

## 8.3 学生管理

### 8.3.1 创建学生
- `POST /students`
- 权限：`school_admin`

### 8.3.2 学生列表
- `GET /students`
- 权限：`platform_admin`、`school_admin`、`teacher`

### 8.3.3 学生详情
- `GET /students/{student_id}`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student(self)`

### 8.3.4 更新学生
- `PUT /students/{student_id}`
- 权限：`school_admin`

### 8.3.5 修改学生状态
- `POST /students/{student_id}/status`
- 权限：`school_admin`

### 8.3.6 获取我的档案
- `GET /students/me/profile`
- 权限：`student`

---

## 8.4 课程与课表管理

### 8.4.1 创建课程
- `POST /courses`
- 权限：`school_admin`

### 8.4.2 课程列表
- `GET /courses`
- 权限：`school_admin`、`teacher`、`student`

### 8.4.3 创建课表记录
- `POST /timetables`
- 权限：`school_admin`

### 8.4.4 查询班级课表
- `GET /timetables/classes/{class_id}`
- 权限：`school_admin`、`teacher`

### 8.4.5 查询教师课表
- `GET /timetables/teachers/{teacher_id}`
- 权限：`school_admin`、`teacher(self)`

### 8.4.6 查询我的课表
- `GET /timetables/me`
- 权限：`student`、`teacher`

---

## 8.5 流程模板配置

### 8.5.1 创建流程模板
- `POST /workflow-templates`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "workflow_type_key": "leave_request",
  "name": "学生请假标准流程",
  "status": "draft",
  "nodes": [
    {
      "node_key": "start_apply",
      "node_name": "提交申请",
      "node_type_key": "start",
      "sort_order": 1
    },
    {
      "node_key": "head_teacher_approve",
      "node_name": "班主任审批",
      "node_type_key": "approval",
      "approver_type_key": "head_teacher",
      "sort_order": 2
    },
    {
      "node_key": "end_finish",
      "node_name": "流程结束",
      "node_type_key": "end",
      "sort_order": 3
    }
  ]
}
```

规则：
- 模板内节点按 `sort_order` 串联。
- 请假流程至少包含 `start`、一个 `approval`、一个 `end`。
- 证明流程允许额外包含 `issue` 节点。

### 8.5.2 流程模板列表
- `GET /workflow-templates`
- 权限：`school_admin`、`teacher`

查询参数：
- `workflow_type_key`
- `status`

### 8.5.3 流程模板详情
- `GET /workflow-templates/{template_id}`
- 权限：`school_admin`、`teacher`

### 8.5.4 更新流程模板
- `PUT /workflow-templates/{template_id}`
- 权限：`school_admin`

### 8.5.5 启用流程模板
- `POST /workflow-templates/{template_id}/activate`
- 权限：`school_admin`

---

## 8.6 学生评教

### 8.6.1 创建评教模板
- `POST /evaluations/templates`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "template_key": "teaching_eval_default",
  "name": "默认课堂评教模板",
  "anonymous_mode": "anonymous",
  "score_scale_type": "five_point",
  "score_min": 1,
  "score_max": 5,
  "dimensions": [
    {
      "dimension_key": "teaching_attitude",
      "dimension_name": "教学态度",
      "weight": 40,
      "score_min": 1,
      "score_max": 5,
      "required": true,
      "comment_enabled": false
    },
    {
      "dimension_key": "teaching_clarity",
      "dimension_name": "讲解清晰度",
      "weight": 40,
      "score_min": 1,
      "score_max": 5,
      "required": true,
      "comment_enabled": false
    },
    {
      "dimension_key": "feedback_comment",
      "dimension_name": "意见建议",
      "weight": 20,
      "score_min": 0,
      "score_max": 5,
      "required": false,
      "comment_enabled": true
    }
  ]
}
```

规则：
- 维度权重总和必须为 `100`。
- 当 `score_scale_type=custom` 时，必须提供模板级 `score_min` 与 `score_max`。

### 8.6.2 评教模板列表
- `GET /evaluations/templates`
- 权限：`school_admin`、`teacher`

### 8.6.3 创建评教任务
- `POST /evaluations/tasks`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "template_id": 701,
  "name": "2026年秋季学期期中评教",
  "target_type": "class",
  "target_ids": [401, 402],
  "anonymous_mode": "anonymous",
  "start_at": "2026-10-01T00:00:00Z",
  "end_at": "2026-10-15T23:59:59Z",
  "status": "published"
}
```

### 8.6.4 评教任务列表
- `GET /evaluations/tasks`
- 权限：`school_admin`、`teacher`、`student`

### 8.6.5 提交评教
- `POST /evaluations/tasks/{task_id}/submissions`
- 权限：`student`

请求示例：

```json
{
  "teacher_id": 501,
  "course_id": 601,
  "answers": [
    {
      "dimension_key": "teaching_attitude",
      "raw_score": 5
    },
    {
      "dimension_key": "teaching_clarity",
      "raw_score": 4
    },
    {
      "dimension_key": "feedback_comment",
      "comment": "希望增加例题讲解。"
    }
  ]
}
```

规则：
- 同一学生对同一评教任务、同一教师、同一课程只允许提交一次。
- 仅在评教任务生效时间内允许提交。

### 8.6.6 查看评教汇总
- `GET /evaluations/tasks/{task_id}/summary`
- 权限：`school_admin`、`teacher`

返回字段：
- `teacher_id`
- `course_id`
- `valid_submission_count`
- `weighted_score`
- `dimension_summary`

---

## 8.7 成绩方案与考试管理

### 8.7.1 创建成绩方案
- `POST /score-schemes`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "course_id": 601,
  "scheme_name": "数学课程总评方案",
  "status": "active",
  "items": [
    {
      "item_key": "usual_score",
      "item_name": "平时成绩",
      "weight": 30,
      "score_type": "numeric",
      "score_min": 0,
      "score_max": 100,
      "decimal_places": 1,
      "is_required": true,
      "counts_in_final": true,
      "allows_makeup": false
    },
    {
      "item_key": "midterm_score",
      "item_name": "期中成绩",
      "weight": 30,
      "score_type": "numeric",
      "score_min": 0,
      "score_max": 100,
      "decimal_places": 1,
      "is_required": true,
      "counts_in_final": true,
      "allows_makeup": true
    },
    {
      "item_key": "final_exam_score",
      "item_name": "期末成绩",
      "weight": 40,
      "score_type": "numeric",
      "score_min": 0,
      "score_max": 100,
      "decimal_places": 1,
      "is_required": true,
      "counts_in_final": true,
      "allows_makeup": true
    }
  ]
}
```

规则：
- 计入总评的成绩项 `counts_in_final=true` 时，权重总和必须为 `100`。

### 8.7.2 成绩方案列表
- `GET /score-schemes`
- 权限：`school_admin`、`teacher`

查询参数：
- `course_id`
- `status`

### 8.7.3 成绩方案详情
- `GET /score-schemes/{scheme_id}`
- 权限：`school_admin`、`teacher`

### 8.7.4 更新成绩方案
- `PUT /score-schemes/{scheme_id}`
- 权限：`school_admin`

### 8.7.5 创建考试
- `POST /exams`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "name": "2026年秋季学期期中考试",
  "term": "2026-fall",
  "class_ids": [401, 402],
  "courses": [
    {
      "course_id": 601,
      "score_scheme_id": 901
    }
  ],
  "start_date": "2026-11-10",
  "end_date": "2026-11-12",
  "status": "draft"
}
```

说明：
- 考试创建后需保存成绩方案快照，后续方案变更不影响历史考试。

### 8.7.6 发布考试
- `POST /exams/{exam_id}/publish`
- 权限：`school_admin`

### 8.7.7 考试列表
- `GET /exams`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student`

### 8.7.8 考试详情
- `GET /exams/{exam_id}`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student`

---

## 8.8 成绩管理

### 8.8.1 批量保存成绩
- `POST /exams/{exam_id}/scores:batch-save`
- 权限：`teacher`、`school_admin`

请求示例：

```json
{
  "course_id": 601,
  "class_id": 401,
  "scores": [
    {
      "student_id": 9001,
      "score_items": [
        {
          "item_key": "usual_score",
          "score_value": 92
        },
        {
          "item_key": "midterm_score",
          "score_value": 90
        },
        {
          "item_key": "final_exam_score",
          "score_value": 95
        }
      ],
      "final_score": 92.6,
      "grade_level": "A",
      "grade_point": 4.0,
      "is_absent": false,
      "is_cheating": false,
      "is_makeup": false,
      "remark": ""
    }
  ]
}
```

规则：
- 教师只能录入自己授课班级和课程的成绩。
- 每个成绩项按考试绑定的方案校验。
- `final_score` 为各计入项按权重汇总后的结果字段。

### 8.8.2 发布成绩
- `POST /exams/{exam_id}/scores/publish`
- 权限：`teacher`、`school_admin`

请求示例：

```json
{
  "course_id": 601,
  "class_id": 401,
  "publish_status": "published"
}
```

### 8.8.3 查询班级成绩
- `GET /exams/{exam_id}/scores`
- 权限：`school_admin`、`teacher`

### 8.8.4 查询学生成绩
- `GET /students/{student_id}/scores`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student(self)`

返回字段补充：
- `score_items`
- `raw_total_score`
- `final_score`
- `grade_level`
- `grade_point`
- `publish_status`
- `published_at`
- `is_absent`
- `is_cheating`
- `is_makeup`

规则：
- 学生端仅返回 `publish_status=published` 的成绩。

### 8.8.5 查询我的成绩
- `GET /students/me/scores`
- 权限：`student`

---

## 8.9 请假管理

### 8.9.1 提交请假申请
- `POST /leave-requests`
- 权限：`student`

请求示例：

```json
{
  "workflow_template_id": 1001,
  "start_at": "2026-09-01T08:00:00Z",
  "end_at": "2026-09-01T18:00:00Z",
  "reason": "就医"
}
```

### 8.9.2 请假申请列表
- `GET /leave-requests`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student`

### 8.9.3 请假详情
- `GET /leave-requests/{leave_request_id}`
- 权限：相关角色可访问

返回字段补充：
- `workflow_template_id`
- `workflow_instance_id`
- `current_node_key`
- `current_node_name`
- `instance_status`
- `available_actions`
- `tasks`
- `action_logs`

### 8.9.4 执行请假流程动作
- `POST /leave-requests/{leave_request_id}/actions`
- 权限：`student`、`teacher`、`school_admin`

请求示例：

```json
{
  "action_key": "approve",
  "comment": "同意"
}
```

说明：
- 学生常用动作：`revoke`、`resubmit`
- 审批人常用动作：`approve`、`reject`

---

## 8.10 证明申请管理

### 8.10.1 创建证明类型
- `POST /certificate-types`
- 权限：`school_admin`

请求示例：

```json
{
  "school_id": 2001,
  "name": "在校证明",
  "description": "用于证明学生当前在校就读",
  "status": "active"
}
```

### 8.10.2 证明类型列表
- `GET /certificate-types`
- 权限：`school_admin`、`student`

### 8.10.3 提交证明申请
- `POST /certificate-requests`
- 权限：`student`

请求示例：

```json
{
  "workflow_template_id": 1101,
  "certificate_type_id": 801,
  "purpose": "奖学金申请",
  "copies": 1
}
```

### 8.10.4 证明申请列表
- `GET /certificate-requests`
- 权限：`platform_admin`、`school_admin`、`teacher`、`student`

### 8.10.5 证明申请详情
- `GET /certificate-requests/{certificate_request_id}`
- 权限：相关角色可访问

返回字段补充：
- `workflow_template_id`
- `workflow_instance_id`
- `current_node_key`
- `current_node_name`
- `instance_status`
- `available_actions`
- `tasks`
- `action_logs`
- `download_url`

### 8.10.6 执行证明流程动作
- `POST /certificate-requests/{certificate_request_id}/actions`
- 权限：`student`、`teacher`、`school_admin`

请求示例：

```json
{
  "action_key": "issue",
  "comment": "已出具"
}
```

说明：
- 证明流程中的 `issue` 通常由学校管理员在出具节点执行。

## 9. 关键业务流程

### 9.1 学生登录并查看课表
1. 学生使用学号和密码登录。
2. 系统返回包含 `student` 角色和 `school_id` 的 token。
3. 学生调用 `GET /timetables/me?term=2026-fall`。
4. 系统根据学生当前班级返回个人课表。

### 9.2 配置请假流程并发起请假
1. 学校管理员创建并启用 `leave_request` 类型流程模板。
2. 学生提交请假申请并选择对应模板。
3. 系统生成流程实例并分发当前待办。
4. 教师或学校管理员执行 `approve` 或 `reject`。
5. 学生在详情中查看当前节点、操作历史和最终状态。

### 9.3 配置证明流程并发起证明申请
1. 学校管理员创建证明类型。
2. 学校管理员创建并启用 `certificate_request` 类型流程模板。
3. 学生提交证明申请。
4. 审批节点处理完成后，学校管理员在出具节点执行 `issue`。
5. 详情返回最终状态和下载地址。

### 9.4 配置评教模板并执行评教
1. 学校管理员创建评教模板，配置维度、权重、分制与匿名模式。
2. 学校管理员创建评教任务并发布。
3. 学生提交对教师和课程的评教结果。
4. 教师查看匿名汇总结果和维度加权分。

### 9.5 绑定成绩方案并发布成绩
1. 学校管理员按课程创建成绩方案。
2. 学校管理员创建考试并为课程绑定成绩方案。
3. 教师录入学生各成绩项分数并生成总评。
4. 教师或学校管理员发布成绩。
5. 学生仅查看已发布成绩。

## 10. 验收检查清单

- 每个接口的角色边界清晰。
- 所有学校级数据都能按 `school_id` 隔离。
- 学校管理员可分别配置请假与证明流程模板。
- 流程模板变更不影响已发起业务的历史流程实例。
- 评教模板支持维度、权重、分制和匿名模式。
- 教师查看匿名评教任务时不暴露学生身份。
- 成绩方案支持课程级自定义成绩项和总评字段。
- 未发布成绩对学生不可见，发布后可查询。
- 考试绑定的成绩方案快照不受后续方案修改影响。
- 文档不依赖具体框架，后续可映射到 FastAPI 或 Django。

## 11. 下一步建议

1. 将本文档进一步转换为 OpenAPI/Swagger 定义。
2. 基于领域模型设计数据库表结构。
3. 细化流程实例、评教汇总、成绩快照的数据表。
4. 选择 FastAPI 或 Django 进行后端脚手架搭建。
