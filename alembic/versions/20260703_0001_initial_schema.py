"""initial schema

Revision ID: 20260703_0001
Revises:
Create Date: 2026-07-03 00:40:00
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import text


revision = "20260703_0001"
down_revision = None
branch_labels = None
depends_on = None


def _split_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        buffer.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(buffer))
            buffer = []

    if buffer:
        statements.append("\n".join(buffer))

    return statements


def upgrade() -> None:
    bind = op.get_bind()
    ddl_path = "docs/schema-v1.mysql.sql"
    ddl_text = open(ddl_path, "r", encoding="utf-8").read()
    statements = _split_statements(ddl_text)

    for statement in statements:
        bind.execute(text(statement))


def downgrade() -> None:
    bind = op.get_bind()
    table_names = [
        "student_score_items",
        "student_score_records",
        "exam_course_score_schemes",
        "exam_courses",
        "exam_classes",
        "exams",
        "score_scheme_items",
        "score_schemes",
        "evaluation_submission_items",
        "evaluation_submissions",
        "evaluation_task_targets",
        "evaluation_tasks",
        "evaluation_dimensions",
        "evaluation_templates",
        "workflow_action_logs",
        "workflow_tasks",
        "workflow_instance_nodes",
        "certificate_requests",
        "leave_requests",
        "workflow_instances",
        "certificate_types",
        "workflow_template_nodes",
        "workflow_templates",
        "timetable_entries",
        "teacher_courses",
        "class_students",
        "student_profiles",
        "classes",
        "teacher_profiles",
        "courses",
        "grades",
        "users",
        "schools",
    ]

    bind.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for table_name in table_names:
        bind.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
    bind.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
