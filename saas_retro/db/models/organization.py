from __future__ import annotations

from datetime import date, time
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, SoftDeleteMixin, TimestampMixin
from ..enums import Status, UserRole


class School(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    contact_name: Mapped[str | None] = mapped_column(String(64))
    contact_phone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    users: Mapped[list["User"]] = relationship(back_populates="school")
    grades: Mapped[list["Grade"]] = relationship(back_populates="school")
    classes: Mapped[list["Classroom"]] = relationship(back_populates="school")
    courses: Mapped[list["Course"]] = relationship(back_populates="school")


class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("role", "login_id", "is_deleted", name="uk_users_role_login"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int | None] = mapped_column(ForeignKey("schools.id"))
    role: Mapped[UserRole] = mapped_column(String(32), nullable=False)
    login_id: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)
    last_login_at: Mapped[date | None]

    school: Mapped[School | None] = relationship(back_populates="users")
    student_profile: Mapped["StudentProfile | None"] = relationship(back_populates="user")
    teacher_profile: Mapped["TeacherProfile | None"] = relationship(back_populates="user")


class Grade(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    school: Mapped[School] = relationship(back_populates="grades")
    classes: Mapped[list["Classroom"]] = relationship(back_populates="grade")
    students: Mapped[list["StudentProfile"]] = relationship(back_populates="grade")


class Course(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (UniqueConstraint("school_id", "code", "is_deleted", name="uk_courses_school_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    credit: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal("0.00"))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    school: Mapped[School] = relationship(back_populates="courses")
    teacher_courses: Mapped[list["TeacherCourse"]] = relationship(back_populates="course")
    timetable_entries: Mapped[list["TimetableEntry"]] = relationship(back_populates="course")


class TeacherProfile(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "teacher_profiles"
    __table_args__ = (
        UniqueConstraint("school_id", "employee_no", "is_deleted", name="uk_teacher_profiles_school_no"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    employee_no: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    user: Mapped[User] = relationship(back_populates="teacher_profile")
    teacher_courses: Mapped[list["TeacherCourse"]] = relationship(back_populates="teacher")
    timetable_entries: Mapped[list["TimetableEntry"]] = relationship(back_populates="teacher")
    head_classes: Mapped[list["Classroom"]] = relationship(back_populates="head_teacher")


class Classroom(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "classes"
    __table_args__ = (
        UniqueConstraint("school_id", "grade_id", "name", "is_deleted", name="uk_classes_school_grade_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    grade_id: Mapped[int] = mapped_column(ForeignKey("grades.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    head_teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teacher_profiles.id"))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    school: Mapped[School] = relationship(back_populates="classes")
    grade: Mapped[Grade] = relationship(back_populates="classes")
    head_teacher: Mapped[TeacherProfile | None] = relationship(back_populates="head_classes")
    students: Mapped[list["StudentProfile"]] = relationship(back_populates="classroom")
    class_students: Mapped[list["ClassStudent"]] = relationship(back_populates="classroom")
    teacher_courses: Mapped[list["TeacherCourse"]] = relationship(back_populates="classroom")
    timetable_entries: Mapped[list["TimetableEntry"]] = relationship(back_populates="classroom")


class StudentProfile(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "student_profiles"
    __table_args__ = (
        UniqueConstraint("school_id", "student_no", "is_deleted", name="uk_student_profiles_school_no"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    student_no: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    gender: Mapped[str | None] = mapped_column(String(16))
    grade_id: Mapped[int] = mapped_column(ForeignKey("grades.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    user: Mapped[User] = relationship(back_populates="student_profile")
    grade: Mapped[Grade] = relationship(back_populates="students")
    classroom: Mapped[Classroom] = relationship(back_populates="students")
    class_students: Mapped[list["ClassStudent"]] = relationship(back_populates="student")


class ClassStudent(TimestampMixin, Base):
    __tablename__ = "class_students"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    is_current: Mapped[bool] = mapped_column(nullable=False, default=True)
    joined_at: Mapped[date | None] = mapped_column(Date())
    left_at: Mapped[date | None] = mapped_column(Date())

    classroom: Mapped[Classroom] = relationship(back_populates="class_students")
    student: Mapped[StudentProfile] = relationship(back_populates="class_students")


class TeacherCourse(TimestampMixin, Base):
    __tablename__ = "teacher_courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher_profiles.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    term: Mapped[str] = mapped_column(String(32), nullable=False)

    teacher: Mapped[TeacherProfile] = relationship(back_populates="teacher_courses")
    course: Mapped[Course] = relationship(back_populates="teacher_courses")
    classroom: Mapped[Classroom] = relationship(back_populates="teacher_courses")


class TimetableEntry(TimestampMixin, Base):
    __tablename__ = "timetable_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    term: Mapped[str] = mapped_column(String(32), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher_profiles.id"), nullable=False)
    weekday: Mapped[int] = mapped_column(nullable=False)
    period: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[time] = mapped_column(Time(), nullable=False)
    end_time: Mapped[time] = mapped_column(Time(), nullable=False)
    location: Mapped[str | None] = mapped_column(String(128))

    classroom: Mapped[Classroom] = relationship(back_populates="timetable_entries")
    course: Mapped[Course] = relationship(back_populates="timetable_entries")
    teacher: Mapped[TeacherProfile] = relationship(back_populates="timetable_entries")
