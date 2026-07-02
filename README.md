# SaaS Retro

当前仓库已整理出一份中文的 V1 需求与接口文档，用于定义一个多学校校园管理 SaaS 的核心后端能力。

## 当前产物

- 需求与接口文档：[docs/api-v1.md](/C:/Users/lenovo/Desktop/SaaS_retro/docs/api-v1.md)
- 数据库表设计文档：[docs/db-schema-v1.md](/C:/Users/lenovo/Desktop/SaaS_retro/docs/db-schema-v1.md)
- MySQL DDL：[docs/schema-v1.mysql.sql](/C:/Users/lenovo/Desktop/SaaS_retro/docs/schema-v1.mysql.sql)

## V1 范围

- 多学校租户模型
- 角色：平台管理员、学校管理员、教师、学生
- 模块：认证、学校与组织、学生、课程、课表、流程模板、学生评教、考试、成绩方案、成绩、请假、证明申请
- 特性：学校可配置流程模板、评教规则、课程级成绩方案

## 建议下一步

1. 基于 DDL 选择 ORM 方案并初始化模型。
2. 基于 Markdown 文档生成 OpenAPI 定义。
3. 选择 Python 后端框架并开始脚手架搭建。
