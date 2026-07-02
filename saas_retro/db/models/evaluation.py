from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import AuditUserMixin, Base, SoftDeleteMixin, TimestampMixin
from ..enums import AnonymousMode, EvaluationTaskStatus, ScoreScaleType


class EvaluationTemplate(TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "evaluation_templates"
    __table_args__ = (
        UniqueConstraint("school_id", "template_key", "is_deleted", name="uk_evaluation_templates_school_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    template_key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    anonymous_mode: Mapped[AnonymousMode] = mapped_column(String(32), nullable=False)
    score_scale_type: Mapped[ScoreScaleType] = mapped_column(String(32), nullable=False)
    score_min: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("0.00"))
    score_max: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("100.00"))
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")

    dimensions: Mapped[list["EvaluationDimension"]] = relationship(back_populates="template")
    tasks: Mapped[list["EvaluationTask"]] = relationship(back_populates="template")


class EvaluationDimension(TimestampMixin, Base):
    __tablename__ = "evaluation_dimensions"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    template_id: Mapped[int] = mapped_column(ForeignKey("evaluation_templates.id"), nullable=False)
    dimension_key: Mapped[str] = mapped_column(String(64), nullable=False)
    dimension_name: Mapped[str] = mapped_column(String(64), nullable=False)
    weight: Mapped[Decimal] = mapped_column(nullable=False)
    score_min: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("0.00"))
    score_max: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("100.00"))
    required_flag: Mapped[bool] = mapped_column(nullable=False, default=True)
    comment_enabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(nullable=False, default=1)

    template: Mapped[EvaluationTemplate] = relationship(back_populates="dimensions")
    submission_items: Mapped[list["EvaluationSubmissionItem"]] = relationship(
        back_populates="dimension"
    )


class EvaluationTask(TimestampMixin, AuditUserMixin, Base):
    __tablename__ = "evaluation_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    template_id: Mapped[int] = mapped_column(ForeignKey("evaluation_templates.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    anonymous_mode: Mapped[AnonymousMode] = mapped_column(String(32), nullable=False)
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    status: Mapped[EvaluationTaskStatus] = mapped_column(String(16), nullable=False)

    template: Mapped[EvaluationTemplate] = relationship(back_populates="tasks")
    targets: Mapped[list["EvaluationTarget"]] = relationship(back_populates="task")
    submissions: Mapped[list["EvaluationSubmission"]] = relationship(back_populates="task")


class EvaluationTarget(Base):
    __tablename__ = "evaluation_task_targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("evaluation_tasks.id"), nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime]

    task: Mapped[EvaluationTask] = relationship(back_populates="targets")


class EvaluationSubmission(TimestampMixin, Base):
    __tablename__ = "evaluation_submissions"
    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "student_id",
            "teacher_id",
            "course_id",
            name="uk_evaluation_submissions_unique",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("evaluation_tasks.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher_profiles.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    weighted_score: Mapped[Decimal | None]
    submitted_at: Mapped[datetime]

    task: Mapped[EvaluationTask] = relationship(back_populates="submissions")
    items: Mapped[list["EvaluationSubmissionItem"]] = relationship(back_populates="submission")


class EvaluationSubmissionItem(TimestampMixin, Base):
    __tablename__ = "evaluation_submission_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id"), nullable=False
    )
    dimension_id: Mapped[int] = mapped_column(ForeignKey("evaluation_dimensions.id"), nullable=False)
    dimension_key: Mapped[str] = mapped_column(String(64), nullable=False)
    dimension_name: Mapped[str] = mapped_column(String(64), nullable=False)
    weight: Mapped[Decimal] = mapped_column(nullable=False)
    raw_score: Mapped[Decimal | None]
    comment: Mapped[str | None]

    submission: Mapped[EvaluationSubmission] = relationship(back_populates="items")
    dimension: Mapped[EvaluationDimension] = relationship(back_populates="submission_items")
