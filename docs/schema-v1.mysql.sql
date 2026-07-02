SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS `schools` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '学校ID',
  `name` VARCHAR(128) NOT NULL COMMENT '学校名称',
  `code` VARCHAR(64) NOT NULL COMMENT '学校编码',
  `contact_name` VARCHAR(64) DEFAULT NULL COMMENT '联系人',
  `contact_phone` VARCHAR(32) DEFAULT NULL COMMENT '联系电话',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_schools_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学校表';

CREATE TABLE IF NOT EXISTS `users` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `school_id` BIGINT DEFAULT NULL COMMENT '学校ID，平台管理员可为空',
  `role` VARCHAR(32) NOT NULL COMMENT '角色',
  `login_id` VARCHAR(64) NOT NULL COMMENT '登录账号',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
  `name` VARCHAR(64) NOT NULL COMMENT '姓名',
  `phone` VARCHAR(32) DEFAULT NULL COMMENT '手机号',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `last_login_at` DATETIME DEFAULT NULL COMMENT '最后登录时间',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_role_login` (`role`, `login_id`, `is_deleted`),
  KEY `idx_users_school_role` (`school_id`, `role`),
  CONSTRAINT `fk_users_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='统一账号表';

CREATE TABLE IF NOT EXISTS `grades` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '年级ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `name` VARCHAR(64) NOT NULL COMMENT '年级名称',
  `academic_year` VARCHAR(32) NOT NULL COMMENT '学年',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_grades_school` (`school_id`),
  CONSTRAINT `fk_grades_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='年级表';

CREATE TABLE IF NOT EXISTS `courses` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '课程ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `name` VARCHAR(128) NOT NULL COMMENT '课程名称',
  `code` VARCHAR(64) NOT NULL COMMENT '课程编码',
  `credit` DECIMAL(6,2) NOT NULL DEFAULT 0.00 COMMENT '学分',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_courses_school_code` (`school_id`, `code`, `is_deleted`),
  CONSTRAINT `fk_courses_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课程表';

CREATE TABLE IF NOT EXISTS `teacher_profiles` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '教师档案ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `employee_no` VARCHAR(64) NOT NULL COMMENT '工号',
  `name` VARCHAR(64) NOT NULL COMMENT '教师姓名',
  `phone` VARCHAR(32) DEFAULT NULL COMMENT '手机号',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_teacher_profiles_school_no` (`school_id`, `employee_no`, `is_deleted`),
  KEY `idx_teacher_profiles_user_id` (`user_id`),
  CONSTRAINT `fk_teacher_profiles_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_teacher_profiles_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='教师档案表';

CREATE TABLE IF NOT EXISTS `classes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '班级ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `grade_id` BIGINT NOT NULL COMMENT '年级ID',
  `name` VARCHAR(64) NOT NULL COMMENT '班级名称',
  `head_teacher_id` BIGINT DEFAULT NULL COMMENT '班主任教师档案ID',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_classes_school_grade_name` (`school_id`, `grade_id`, `name`, `is_deleted`),
  KEY `idx_classes_head_teacher_id` (`head_teacher_id`),
  CONSTRAINT `fk_classes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_classes_grade_id` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`),
  CONSTRAINT `fk_classes_head_teacher_id` FOREIGN KEY (`head_teacher_id`) REFERENCES `teacher_profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='班级表';

CREATE TABLE IF NOT EXISTS `student_profiles` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '学生档案ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `student_no` VARCHAR(64) NOT NULL COMMENT '学号',
  `name` VARCHAR(64) NOT NULL COMMENT '学生姓名',
  `gender` VARCHAR(16) DEFAULT NULL COMMENT '性别',
  `grade_id` BIGINT NOT NULL COMMENT '当前年级',
  `class_id` BIGINT NOT NULL COMMENT '当前班级',
  `phone` VARCHAR(32) DEFAULT NULL COMMENT '联系电话',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_student_profiles_school_no` (`school_id`, `student_no`, `is_deleted`),
  KEY `idx_student_profiles_class` (`class_id`),
  KEY `idx_student_profiles_user_id` (`user_id`),
  CONSTRAINT `fk_student_profiles_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_student_profiles_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_student_profiles_grade_id` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`),
  CONSTRAINT `fk_student_profiles_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生档案表';

CREATE TABLE IF NOT EXISTS `class_students` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `class_id` BIGINT NOT NULL COMMENT '班级ID',
  `student_id` BIGINT NOT NULL COMMENT '学生档案ID',
  `is_current` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否当前班级',
  `joined_at` DATE DEFAULT NULL COMMENT '入班日期',
  `left_at` DATE DEFAULT NULL COMMENT '离班日期',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_class_students_class_id` (`class_id`),
  KEY `idx_class_students_student_id` (`student_id`),
  CONSTRAINT `fk_class_students_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_class_students_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`),
  CONSTRAINT `fk_class_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生班级关系表';

CREATE TABLE IF NOT EXISTS `teacher_courses` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `teacher_id` BIGINT NOT NULL COMMENT '教师档案ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `class_id` BIGINT NOT NULL COMMENT '班级ID',
  `term` VARCHAR(32) NOT NULL COMMENT '学期',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_teacher_courses_teacher_term` (`teacher_id`, `term`),
  KEY `idx_teacher_courses_class_course` (`class_id`, `course_id`, `term`),
  CONSTRAINT `fk_teacher_courses_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_teacher_courses_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_profiles` (`id`),
  CONSTRAINT `fk_teacher_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_teacher_courses_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='教师授课关系表';

CREATE TABLE IF NOT EXISTS `timetable_entries` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '课表记录ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `term` VARCHAR(32) NOT NULL COMMENT '学期',
  `class_id` BIGINT NOT NULL COMMENT '班级ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `teacher_id` BIGINT NOT NULL COMMENT '教师档案ID',
  `weekday` TINYINT NOT NULL COMMENT '星期几',
  `period` TINYINT NOT NULL COMMENT '第几节',
  `start_time` TIME NOT NULL COMMENT '开始时间',
  `end_time` TIME NOT NULL COMMENT '结束时间',
  `location` VARCHAR(128) DEFAULT NULL COMMENT '上课地点',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_timetable_entries_class_term` (`class_id`, `term`),
  KEY `idx_timetable_entries_teacher_term` (`teacher_id`, `term`),
  CONSTRAINT `fk_timetable_entries_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_timetable_entries_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`),
  CONSTRAINT `fk_timetable_entries_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_timetable_entries_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课表表';

CREATE TABLE IF NOT EXISTS `workflow_templates` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '模板ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `workflow_type_key` VARCHAR(64) NOT NULL COMMENT '流程类型',
  `name` VARCHAR(128) NOT NULL COMMENT '模板名称',
  `status` VARCHAR(16) NOT NULL DEFAULT 'draft' COMMENT '模板状态',
  `version` INT NOT NULL DEFAULT 1 COMMENT '模板版本号',
  `created_by` BIGINT NOT NULL COMMENT '创建人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_templates_school_type` (`school_id`, `workflow_type_key`, `status`),
  CONSTRAINT `fk_workflow_templates_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_templates_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_workflow_templates_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程模板表';

CREATE TABLE IF NOT EXISTS `workflow_template_nodes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '节点ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `template_id` BIGINT NOT NULL COMMENT '流程模板ID',
  `node_key` VARCHAR(64) NOT NULL COMMENT '节点编码',
  `node_name` VARCHAR(64) NOT NULL COMMENT '节点名称',
  `node_type_key` VARCHAR(32) NOT NULL COMMENT '节点类型',
  `approver_type_key` VARCHAR(32) DEFAULT NULL COMMENT '审批人类型',
  `sort_order` INT NOT NULL COMMENT '顺序',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_workflow_template_nodes_template_key` (`template_id`, `node_key`),
  KEY `idx_workflow_template_nodes_template_sort` (`template_id`, `sort_order`),
  CONSTRAINT `fk_workflow_template_nodes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_template_nodes_template_id` FOREIGN KEY (`template_id`) REFERENCES `workflow_templates` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程模板节点表';

CREATE TABLE IF NOT EXISTS `certificate_types` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '证明类型ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `name` VARCHAR(128) NOT NULL COMMENT '证明名称',
  `description` VARCHAR(255) DEFAULT NULL COMMENT '描述',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_certificate_types_school_status` (`school_id`, `status`),
  CONSTRAINT `fk_certificate_types_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='证明类型表';

CREATE TABLE IF NOT EXISTS `workflow_instances` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '流程实例ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `workflow_type_key` VARCHAR(64) NOT NULL COMMENT '流程类型',
  `template_id` BIGINT NOT NULL COMMENT '模板ID',
  `template_version` INT NOT NULL COMMENT '模板版本快照',
  `business_type` VARCHAR(64) NOT NULL COMMENT '业务类型',
  `business_id` BIGINT NOT NULL COMMENT '业务单据ID',
  `current_node_key` VARCHAR(64) DEFAULT NULL COMMENT '当前节点编码',
  `current_node_name` VARCHAR(64) DEFAULT NULL COMMENT '当前节点名称',
  `instance_status` VARCHAR(32) NOT NULL COMMENT '流程状态',
  `started_by` BIGINT NOT NULL COMMENT '发起人',
  `started_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发起时间',
  `finished_at` DATETIME DEFAULT NULL COMMENT '完成时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_workflow_instances_business` (`business_type`, `business_id`),
  KEY `idx_workflow_instances_school_status` (`school_id`, `instance_status`),
  CONSTRAINT `fk_workflow_instances_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_instances_template_id` FOREIGN KEY (`template_id`) REFERENCES `workflow_templates` (`id`),
  CONSTRAINT `fk_workflow_instances_started_by` FOREIGN KEY (`started_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程实例表';

CREATE TABLE IF NOT EXISTS `leave_requests` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '请假单ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `student_id` BIGINT NOT NULL COMMENT '学生档案ID',
  `workflow_template_id` BIGINT NOT NULL COMMENT '流程模板ID',
  `workflow_instance_id` BIGINT DEFAULT NULL COMMENT '流程实例ID',
  `start_at` DATETIME NOT NULL COMMENT '开始时间',
  `end_at` DATETIME NOT NULL COMMENT '结束时间',
  `reason` VARCHAR(255) NOT NULL COMMENT '请假原因',
  `instance_status` VARCHAR(32) NOT NULL COMMENT '流程状态',
  `created_by` BIGINT NOT NULL COMMENT '发起人用户ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_leave_requests_student_status` (`student_id`, `instance_status`),
  CONSTRAINT `fk_leave_requests_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_leave_requests_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`),
  CONSTRAINT `fk_leave_requests_workflow_template_id` FOREIGN KEY (`workflow_template_id`) REFERENCES `workflow_templates` (`id`),
  CONSTRAINT `fk_leave_requests_workflow_instance_id` FOREIGN KEY (`workflow_instance_id`) REFERENCES `workflow_instances` (`id`),
  CONSTRAINT `fk_leave_requests_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='请假申请表';

CREATE TABLE IF NOT EXISTS `certificate_requests` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '证明申请ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `student_id` BIGINT NOT NULL COMMENT '学生档案ID',
  `certificate_type_id` BIGINT NOT NULL COMMENT '证明类型ID',
  `workflow_template_id` BIGINT NOT NULL COMMENT '流程模板ID',
  `workflow_instance_id` BIGINT DEFAULT NULL COMMENT '流程实例ID',
  `purpose` VARCHAR(255) NOT NULL COMMENT '申请用途',
  `copies` INT NOT NULL DEFAULT 1 COMMENT '申请份数',
  `instance_status` VARCHAR(32) NOT NULL COMMENT '流程状态',
  `download_url` VARCHAR(255) DEFAULT NULL COMMENT '下载地址',
  `created_by` BIGINT NOT NULL COMMENT '发起人用户ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_certificate_requests_student_status` (`student_id`, `instance_status`),
  CONSTRAINT `fk_certificate_requests_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_certificate_requests_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`),
  CONSTRAINT `fk_certificate_requests_certificate_type_id` FOREIGN KEY (`certificate_type_id`) REFERENCES `certificate_types` (`id`),
  CONSTRAINT `fk_certificate_requests_workflow_template_id` FOREIGN KEY (`workflow_template_id`) REFERENCES `workflow_templates` (`id`),
  CONSTRAINT `fk_certificate_requests_workflow_instance_id` FOREIGN KEY (`workflow_instance_id`) REFERENCES `workflow_instances` (`id`),
  CONSTRAINT `fk_certificate_requests_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='证明申请表';

CREATE TABLE IF NOT EXISTS `workflow_instance_nodes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `instance_id` BIGINT NOT NULL COMMENT '流程实例ID',
  `node_key` VARCHAR(64) NOT NULL COMMENT '节点编码',
  `node_name` VARCHAR(64) NOT NULL COMMENT '节点名称',
  `node_type_key` VARCHAR(32) NOT NULL COMMENT '节点类型',
  `approver_type_key` VARCHAR(32) DEFAULT NULL COMMENT '审批人类型',
  `sort_order` INT NOT NULL COMMENT '排序',
  `node_status` VARCHAR(32) NOT NULL COMMENT '节点状态',
  `started_at` DATETIME DEFAULT NULL COMMENT '开始时间',
  `finished_at` DATETIME DEFAULT NULL COMMENT '结束时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_instance_nodes_instance_sort` (`instance_id`, `sort_order`),
  CONSTRAINT `fk_workflow_instance_nodes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_instance_nodes_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `workflow_instances` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程实例节点快照表';

CREATE TABLE IF NOT EXISTS `workflow_tasks` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `instance_id` BIGINT NOT NULL COMMENT '流程实例ID',
  `business_type` VARCHAR(64) NOT NULL COMMENT '业务类型',
  `business_id` BIGINT NOT NULL COMMENT '业务单据ID',
  `node_key` VARCHAR(64) NOT NULL COMMENT '节点编码',
  `node_name` VARCHAR(64) NOT NULL COMMENT '节点名称',
  `approver_type_key` VARCHAR(32) NOT NULL COMMENT '审批人类型',
  `assignee_user_id` BIGINT DEFAULT NULL COMMENT '实际处理人',
  `task_status` VARCHAR(32) NOT NULL COMMENT '任务状态',
  `actioned_at` DATETIME DEFAULT NULL COMMENT '处理时间',
  `comment` VARCHAR(255) DEFAULT NULL COMMENT '处理意见',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_tasks_instance_status` (`instance_id`, `task_status`),
  KEY `idx_workflow_tasks_assignee` (`assignee_user_id`, `task_status`),
  CONSTRAINT `fk_workflow_tasks_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_tasks_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `workflow_instances` (`id`),
  CONSTRAINT `fk_workflow_tasks_assignee_user_id` FOREIGN KEY (`assignee_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程待办表';

CREATE TABLE IF NOT EXISTS `workflow_action_logs` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `instance_id` BIGINT NOT NULL COMMENT '流程实例ID',
  `business_type` VARCHAR(64) NOT NULL COMMENT '业务类型',
  `business_id` BIGINT NOT NULL COMMENT '业务单据ID',
  `node_key` VARCHAR(64) DEFAULT NULL COMMENT '操作节点',
  `action_key` VARCHAR(32) NOT NULL COMMENT '动作关键字',
  `operator_user_id` BIGINT NOT NULL COMMENT '操作人用户ID',
  `operator_role` VARCHAR(32) NOT NULL COMMENT '操作人角色',
  `comment` VARCHAR(255) DEFAULT NULL COMMENT '操作意见',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_action_logs_instance` (`instance_id`, `created_at`),
  CONSTRAINT `fk_workflow_action_logs_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_workflow_action_logs_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `workflow_instances` (`id`),
  CONSTRAINT `fk_workflow_action_logs_operator_user_id` FOREIGN KEY (`operator_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程操作日志表';

CREATE TABLE IF NOT EXISTS `evaluation_templates` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '模板ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `template_key` VARCHAR(64) NOT NULL COMMENT '模板编码',
  `name` VARCHAR(128) NOT NULL COMMENT '模板名称',
  `anonymous_mode` VARCHAR(32) NOT NULL COMMENT '匿名模式',
  `score_scale_type` VARCHAR(32) NOT NULL COMMENT '分制类型',
  `score_min` DECIMAL(8,2) NOT NULL DEFAULT 0.00 COMMENT '最小分',
  `score_max` DECIMAL(8,2) NOT NULL DEFAULT 100.00 COMMENT '最大分',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `created_by` BIGINT NOT NULL COMMENT '创建人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_evaluation_templates_school_key` (`school_id`, `template_key`, `is_deleted`),
  CONSTRAINT `fk_evaluation_templates_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_templates_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_evaluation_templates_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教模板表';

CREATE TABLE IF NOT EXISTS `evaluation_dimensions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '维度ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `template_id` BIGINT NOT NULL COMMENT '模板ID',
  `dimension_key` VARCHAR(64) NOT NULL COMMENT '维度编码',
  `dimension_name` VARCHAR(64) NOT NULL COMMENT '维度名称',
  `weight` DECIMAL(6,2) NOT NULL COMMENT '权重',
  `score_min` DECIMAL(8,2) NOT NULL DEFAULT 0.00 COMMENT '最小分',
  `score_max` DECIMAL(8,2) NOT NULL DEFAULT 100.00 COMMENT '最大分',
  `required_flag` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否必填',
  `comment_enabled` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否允许文本意见',
  `sort_order` INT NOT NULL DEFAULT 1 COMMENT '排序',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_evaluation_dimensions_template_sort` (`template_id`, `sort_order`),
  CONSTRAINT `fk_evaluation_dimensions_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_dimensions_template_id` FOREIGN KEY (`template_id`) REFERENCES `evaluation_templates` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教维度表';

CREATE TABLE IF NOT EXISTS `evaluation_tasks` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `template_id` BIGINT NOT NULL COMMENT '模板ID',
  `name` VARCHAR(128) NOT NULL COMMENT '任务名称',
  `target_type` VARCHAR(32) NOT NULL COMMENT '目标类型',
  `anonymous_mode` VARCHAR(32) NOT NULL COMMENT '匿名模式',
  `start_at` DATETIME NOT NULL COMMENT '开始时间',
  `end_at` DATETIME NOT NULL COMMENT '结束时间',
  `status` VARCHAR(16) NOT NULL DEFAULT 'draft' COMMENT '状态',
  `created_by` BIGINT NOT NULL COMMENT '创建人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_evaluation_tasks_school_status` (`school_id`, `status`),
  CONSTRAINT `fk_evaluation_tasks_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_tasks_template_id` FOREIGN KEY (`template_id`) REFERENCES `evaluation_templates` (`id`),
  CONSTRAINT `fk_evaluation_tasks_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_evaluation_tasks_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教任务表';

CREATE TABLE IF NOT EXISTS `evaluation_task_targets` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `task_id` BIGINT NOT NULL COMMENT '任务ID',
  `target_type` VARCHAR(32) NOT NULL COMMENT '目标类型',
  `target_id` BIGINT NOT NULL COMMENT '目标ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_evaluation_task_targets_task_id` (`task_id`),
  CONSTRAINT `fk_evaluation_task_targets_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_task_targets_task_id` FOREIGN KEY (`task_id`) REFERENCES `evaluation_tasks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教任务目标范围表';

CREATE TABLE IF NOT EXISTS `evaluation_submissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '提交ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `task_id` BIGINT NOT NULL COMMENT '任务ID',
  `student_id` BIGINT NOT NULL COMMENT '学生档案ID',
  `teacher_id` BIGINT NOT NULL COMMENT '教师档案ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `weighted_score` DECIMAL(8,2) DEFAULT NULL COMMENT '加权总分',
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_evaluation_submissions_unique` (`task_id`, `student_id`, `teacher_id`, `course_id`),
  CONSTRAINT `fk_evaluation_submissions_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_submissions_task_id` FOREIGN KEY (`task_id`) REFERENCES `evaluation_tasks` (`id`),
  CONSTRAINT `fk_evaluation_submissions_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`),
  CONSTRAINT `fk_evaluation_submissions_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_profiles` (`id`),
  CONSTRAINT `fk_evaluation_submissions_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教提交主表';

CREATE TABLE IF NOT EXISTS `evaluation_submission_items` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `submission_id` BIGINT NOT NULL COMMENT '提交ID',
  `dimension_id` BIGINT NOT NULL COMMENT '维度ID',
  `dimension_key` VARCHAR(64) NOT NULL COMMENT '维度编码快照',
  `dimension_name` VARCHAR(64) NOT NULL COMMENT '维度名称快照',
  `weight` DECIMAL(6,2) NOT NULL COMMENT '权重快照',
  `raw_score` DECIMAL(8,2) DEFAULT NULL COMMENT '原始分值',
  `comment` TEXT DEFAULT NULL COMMENT '文本意见',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_evaluation_submission_items_submission_id` (`submission_id`),
  CONSTRAINT `fk_evaluation_submission_items_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_evaluation_submission_items_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`),
  CONSTRAINT `fk_evaluation_submission_items_dimension_id` FOREIGN KEY (`dimension_id`) REFERENCES `evaluation_dimensions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评教提交明细表';

CREATE TABLE IF NOT EXISTS `score_schemes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '方案ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `scheme_name` VARCHAR(128) NOT NULL COMMENT '方案名称',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '状态',
  `version` INT NOT NULL DEFAULT 1 COMMENT '方案版本号',
  `created_by` BIGINT NOT NULL COMMENT '创建人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_score_schemes_school_course_status` (`school_id`, `course_id`, `status`),
  CONSTRAINT `fk_score_schemes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_score_schemes_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_score_schemes_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_score_schemes_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成绩方案表';

CREATE TABLE IF NOT EXISTS `score_scheme_items` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '成绩项ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `scheme_id` BIGINT NOT NULL COMMENT '成绩方案ID',
  `item_key` VARCHAR(64) NOT NULL COMMENT '成绩项编码',
  `item_name` VARCHAR(64) NOT NULL COMMENT '成绩项名称',
  `weight` DECIMAL(6,2) NOT NULL DEFAULT 0.00 COMMENT '权重',
  `score_type` VARCHAR(32) NOT NULL COMMENT '成绩项类型',
  `score_min` DECIMAL(8,2) DEFAULT NULL COMMENT '最小分',
  `score_max` DECIMAL(8,2) DEFAULT NULL COMMENT '最大分',
  `decimal_places` TINYINT NOT NULL DEFAULT 1 COMMENT '小数位数',
  `is_required` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否必填',
  `counts_in_final` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否计入总评',
  `allows_makeup` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否允许补考',
  `sort_order` INT NOT NULL DEFAULT 1 COMMENT '排序',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_score_scheme_items_scheme_key` (`scheme_id`, `item_key`),
  KEY `idx_score_scheme_items_scheme_sort` (`scheme_id`, `sort_order`),
  CONSTRAINT `fk_score_scheme_items_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_score_scheme_items_scheme_id` FOREIGN KEY (`scheme_id`) REFERENCES `score_schemes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成绩方案明细表';

CREATE TABLE IF NOT EXISTS `exams` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '考试ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `name` VARCHAR(128) NOT NULL COMMENT '考试名称',
  `term` VARCHAR(32) NOT NULL COMMENT '学期',
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE NOT NULL COMMENT '结束日期',
  `status` VARCHAR(16) NOT NULL DEFAULT 'draft' COMMENT '状态',
  `created_by` BIGINT NOT NULL COMMENT '创建人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_exams_school_term_status` (`school_id`, `term`, `status`),
  CONSTRAINT `fk_exams_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_exams_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_exams_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='考试表';

CREATE TABLE IF NOT EXISTS `exam_classes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `exam_id` BIGINT NOT NULL COMMENT '考试ID',
  `class_id` BIGINT NOT NULL COMMENT '班级ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_exam_classes_exam_class` (`exam_id`, `class_id`),
  CONSTRAINT `fk_exam_classes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_exam_classes_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  CONSTRAINT `fk_exam_classes_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='考试班级关联表';

CREATE TABLE IF NOT EXISTS `exam_courses` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `exam_id` BIGINT NOT NULL COMMENT '考试ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `score_scheme_id` BIGINT NOT NULL COMMENT '原方案ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_exam_courses_exam_course` (`exam_id`, `course_id`),
  CONSTRAINT `fk_exam_courses_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_exam_courses_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  CONSTRAINT `fk_exam_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_exam_courses_score_scheme_id` FOREIGN KEY (`score_scheme_id`) REFERENCES `score_schemes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='考试课程关联表';

CREATE TABLE IF NOT EXISTS `exam_course_score_schemes` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `exam_id` BIGINT NOT NULL COMMENT '考试ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `source_scheme_id` BIGINT NOT NULL COMMENT '来源成绩方案ID',
  `source_scheme_version` INT NOT NULL COMMENT '来源方案版本',
  `scheme_name` VARCHAR(128) NOT NULL COMMENT '方案名称快照',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '快照状态',
  `snapshot_json` JSON NOT NULL COMMENT '方案快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_exam_course_score_schemes_exam_course` (`exam_id`, `course_id`),
  CONSTRAINT `fk_exam_course_score_schemes_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_exam_course_score_schemes_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  CONSTRAINT `fk_exam_course_score_schemes_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_exam_course_score_schemes_source_scheme_id` FOREIGN KEY (`source_scheme_id`) REFERENCES `score_schemes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='考试课程成绩方案快照表';

CREATE TABLE IF NOT EXISTS `student_score_records` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '成绩记录ID',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `exam_id` BIGINT NOT NULL COMMENT '考试ID',
  `class_id` BIGINT NOT NULL COMMENT '班级ID',
  `student_id` BIGINT NOT NULL COMMENT '学生档案ID',
  `course_id` BIGINT NOT NULL COMMENT '课程ID',
  `scheme_snapshot_id` BIGINT NOT NULL COMMENT '方案快照ID',
  `raw_total_score` DECIMAL(8,2) DEFAULT NULL COMMENT '原始累计分',
  `final_score` DECIMAL(8,2) DEFAULT NULL COMMENT '总评分',
  `grade_level` VARCHAR(32) DEFAULT NULL COMMENT '等级',
  `grade_point` DECIMAL(6,2) DEFAULT NULL COMMENT '绩点',
  `publish_status` VARCHAR(16) NOT NULL DEFAULT 'draft' COMMENT '发布状态',
  `published_at` DATETIME DEFAULT NULL COMMENT '发布时间',
  `is_absent` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否缺考',
  `is_cheating` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否作弊',
  `is_makeup` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否补考',
  `remark` VARCHAR(255) DEFAULT NULL COMMENT '备注',
  `created_by` BIGINT NOT NULL COMMENT '录入人',
  `updated_by` BIGINT NOT NULL COMMENT '更新人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_student_score_records_exam_student_course` (`exam_id`, `student_id`, `course_id`),
  KEY `idx_student_score_records_student` (`student_id`, `publish_status`),
  CONSTRAINT `fk_student_score_records_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_student_score_records_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  CONSTRAINT `fk_student_score_records_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`),
  CONSTRAINT `fk_student_score_records_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`),
  CONSTRAINT `fk_student_score_records_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `fk_student_score_records_scheme_snapshot_id` FOREIGN KEY (`scheme_snapshot_id`) REFERENCES `exam_course_score_schemes` (`id`),
  CONSTRAINT `fk_student_score_records_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_student_score_records_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生成绩主记录表';

CREATE TABLE IF NOT EXISTS `student_score_items` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `school_id` BIGINT NOT NULL COMMENT '学校ID',
  `score_record_id` BIGINT NOT NULL COMMENT '成绩主记录ID',
  `item_key` VARCHAR(64) NOT NULL COMMENT '成绩项编码快照',
  `item_name` VARCHAR(64) NOT NULL COMMENT '成绩项名称快照',
  `weight` DECIMAL(6,2) NOT NULL DEFAULT 0.00 COMMENT '权重快照',
  `score_type` VARCHAR(32) NOT NULL COMMENT '成绩项类型',
  `score_value` DECIMAL(8,2) DEFAULT NULL COMMENT '数值分',
  `grade_value` VARCHAR(32) DEFAULT NULL COMMENT '等级值',
  `pass_flag` TINYINT(1) DEFAULT NULL COMMENT '合格标记',
  `counts_in_final` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否计入总评',
  `remark` VARCHAR(255) DEFAULT NULL COMMENT '备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_student_score_items_score_record_id` (`score_record_id`),
  CONSTRAINT `fk_student_score_items_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_student_score_items_score_record_id` FOREIGN KEY (`score_record_id`) REFERENCES `student_score_records` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生成绩分项明细表';

SET FOREIGN_KEY_CHECKS = 1;
