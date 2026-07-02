from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import AuditUserMixin, Base, SoftDeleteMixin, TimestampMixin
from ..enums import ExamStatus, PublishStatus, ScoreType


class ScoreScheme(TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "score_schemes"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    scheme_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    version: Mapped[int] = mapped_column(nullable=False, default=1)

    items: Mapped[list["ScoreSchemeItem"]] = relationship(back_populates="scheme")
    exam_courses: Mapped[list["ExamCourse"]] = relationship(back_populates="score_scheme")
    snapshots: Mapped[list["ExamCourseScoreScheme"]] = relationship(back_populates="source_scheme")


class ScoreSchemeItem(TimestampMixin, Base):
    __tablename__ = "score_scheme_items"
    __table_args__ = (
        UniqueConstraint("scheme_id", "item_key", name="uk_score_scheme_items_scheme_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    scheme_id: Mapped[int] = mapped_column(ForeignKey("score_schemes.id"), nullable=False)
    item_key: Mapped[str] = mapped_column(String(64), nullable=False)
    item_name: Mapped[str] = mapped_column(String(64), nullable=False)
    weight: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("0.00"))
    score_type: Mapped[ScoreType] = mapped_column(String(32), nullable=False)
    score_min: Mapped[Decimal | None]
    score_max: Mapped[Decimal | None]
    decimal_places: Mapped[int] = mapped_column(nullable=False, default=1)
    is_required: Mapped[bool] = mapped_column(nullable=False, default=True)
    counts_in_final: Mapped[bool] = mapped_column(nullable=False, default=True)
    allows_makeup: Mapped[bool] = mapped_column(nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(nullable=False, default=1)

    scheme: Mapped[ScoreScheme] = relationship(back_populates="items")


class Exam(TimestampMixin, AuditUserMixin, Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    term: Mapped[str] = mapped_column(String(32), nullable=False)
    start_date: Mapped[date]
    end_date: Mapped[date]
    status: Mapped[ExamStatus] = mapped_column(String(16), nullable=False, default=ExamStatus.DRAFT)

    exam_classes: Mapped[list["ExamClass"]] = relationship(back_populates="exam")
    exam_courses: Mapped[list["ExamCourse"]] = relationship(back_populates="exam")
    course_snapshots: Mapped[list["ExamCourseScoreScheme"]] = relationship(back_populates="exam")
    score_records: Mapped[list["StudentScoreRecord"]] = relationship(back_populates="exam")


class ExamClass(Base):
    __tablename__ = "exam_classes"
    __table_args__ = (UniqueConstraint("exam_id", "class_id", name="uk_exam_classes_exam_class"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    created_at: Mapped[datetime]

    exam: Mapped[Exam] = relationship(back_populates="exam_classes")


class ExamCourse(Base):
    __tablename__ = "exam_courses"
    __table_args__ = (UniqueConstraint("exam_id", "course_id", name="uk_exam_courses_exam_course"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    score_scheme_id: Mapped[int] = mapped_column(ForeignKey("score_schemes.id"), nullable=False)
    created_at: Mapped[datetime]

    exam: Mapped[Exam] = relationship(back_populates="exam_courses")
    score_scheme: Mapped[ScoreScheme] = relationship(back_populates="exam_courses")


class ExamCourseScoreScheme(TimestampMixin, Base):
    __tablename__ = "exam_course_score_schemes"
    __table_args__ = (
        UniqueConstraint("exam_id", "course_id", name="uk_exam_course_score_schemes_exam_course"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    source_scheme_id: Mapped[int] = mapped_column(ForeignKey("score_schemes.id"), nullable=False)
    source_scheme_version: Mapped[int] = mapped_column(nullable=False)
    scheme_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    snapshot_json: Mapped[dict[str, object]]

    exam: Mapped[Exam] = relationship(back_populates="course_snapshots")
    source_scheme: Mapped[ScoreScheme] = relationship(back_populates="snapshots")
    score_records: Mapped[list["StudentScoreRecord"]] = relationship(back_populates="scheme_snapshot")


class StudentScoreRecord(TimestampMixin, AuditUserMixin, Base):
    __tablename__ = "student_score_records"
    __table_args__ = (
        UniqueConstraint("exam_id", "student_id", "course_id", name="uk_student_score_records_exam_student_course"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    scheme_snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("exam_course_score_schemes.id"), nullable=False
    )
    raw_total_score: Mapped[Decimal | None]
    final_score: Mapped[Decimal | None]
    grade_level: Mapped[str | None] = mapped_column(String(32))
    grade_point: Mapped[Decimal | None]
    publish_status: Mapped[PublishStatus] = mapped_column(
        String(16), nullable=False, default=PublishStatus.DRAFT
    )
    published_at: Mapped[datetime | None]
    is_absent: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_cheating: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_makeup: Mapped[bool] = mapped_column(nullable=False, default=False)
    remark: Mapped[str | None] = mapped_column(String(255))

    exam: Mapped[Exam] = relationship(back_populates="score_records")
    scheme_snapshot: Mapped[ExamCourseScoreScheme] = relationship(back_populates="score_records")
    items: Mapped[list["StudentScoreItem"]] = relationship(back_populates="score_record")


class StudentScoreItem(TimestampMixin, Base):
    __tablename__ = "student_score_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    score_record_id: Mapped[int] = mapped_column(
        ForeignKey("student_score_records.id"), nullable=False
    )
    item_key: Mapped[str] = mapped_column(String(64), nullable=False)
    item_name: Mapped[str] = mapped_column(String(64), nullable=False)
    weight: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("0.00"))
    score_type: Mapped[ScoreType] = mapped_column(String(32), nullable=False)
    score_value: Mapped[Decimal | None]
    grade_value: Mapped[str | None] = mapped_column(String(32))
    pass_flag: Mapped[bool | None]
    counts_in_final: Mapped[bool] = mapped_column(nullable=False, default=True)
    remark: Mapped[str | None] = mapped_column(String(255))

    score_record: Mapped[StudentScoreRecord] = relationship(back_populates="items")
