from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from saas_retro.api.deps import get_current_user, get_db_session, require_roles
from saas_retro.api.schemas.common import ApiResponse, PageResponse
from saas_retro.api.schemas.student import StudentListQuery
from saas_retro.api.schemas.student import (
    StudentCreateRequest,
    StudentResponse,
    StudentStatusUpdateRequest,
    StudentUpdateRequest,
)
from saas_retro.core.security import hash_password
from saas_retro.db.enums import UserRole
from saas_retro.db.models.organization import (
    ClassStudent,
    Classroom,
    Grade,
    StudentProfile,
    TeacherCourse,
    TeacherProfile,
    User,
)

router = APIRouter(prefix="/api/v1/students", tags=["students"])


def _require_school_scope(current_user: User) -> int:
    if current_user.school_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="School scope required")
    return current_user.school_id


def _get_student_or_404(session: Session, student_id: int) -> StudentProfile:
    student = session.get(StudentProfile, student_id)
    if student is None or student.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


def _ensure_student_in_school(student: StudentProfile, school_id: int) -> None:
    if student.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")


def _teacher_accessible_class_ids(session: Session, current_user: User) -> set[int]:
    stmt = select(TeacherProfile.id).where(
        TeacherProfile.user_id == current_user.id,
        TeacherProfile.school_id == current_user.school_id,
        TeacherProfile.is_deleted.is_(False),
    )
    teacher_id = session.execute(stmt).scalar_one_or_none()
    if teacher_id is None:
        return set()

    class_stmt = select(TeacherCourse.class_id).where(
        TeacherCourse.teacher_id == teacher_id,
        TeacherCourse.school_id == current_user.school_id,
    )
    return set(session.execute(class_stmt).scalars().all())


@router.post("", response_model=ApiResponse[StudentResponse])
def create_student(
    payload: StudentCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[StudentResponse]:
    school_id = _require_school_scope(current_user)

    grade = session.get(Grade, payload.grade_id)
    classroom = session.get(Classroom, payload.class_id)
    if grade is None or grade.is_deleted or grade.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade")
    if classroom is None or classroom.is_deleted or classroom.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid class")

    existing_user = session.execute(
        select(User).where(
            User.role == UserRole.STUDENT,
            User.login_id == payload.student_no,
            User.is_deleted.is_(False),
        )
    ).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student login already exists")

    existing_student = session.execute(
        select(StudentProfile).where(
            StudentProfile.school_id == school_id,
            StudentProfile.student_no == payload.student_no,
            StudentProfile.is_deleted.is_(False),
        )
    ).scalar_one_or_none()
    if existing_student is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student number already exists")

    user = User(
        school_id=school_id,
        role=UserRole.STUDENT,
        login_id=payload.student_no,
        password_hash=hash_password(payload.password),
        name=payload.name,
        phone=payload.phone,
        status=payload.status,
    )
    session.add(user)
    session.flush()

    student = StudentProfile(
        school_id=school_id,
        user_id=user.id,
        student_no=payload.student_no,
        name=payload.name,
        gender=payload.gender,
        grade_id=payload.grade_id,
        class_id=payload.class_id,
        phone=payload.phone,
        status=payload.status,
    )
    session.add(student)
    session.flush()

    session.add(
        ClassStudent(
            school_id=school_id,
            class_id=payload.class_id,
            student_id=student.id,
            is_current=True,
        )
    )
    session.commit()
    session.refresh(student)
    return ApiResponse.ok(StudentResponse.model_validate(student))


@router.get("", response_model=ApiResponse[PageResponse[StudentResponse]])
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    grade_id: int | None = Query(default=None),
    class_id: int | None = Query(default=None),
    keyword: str | None = Query(default=None),
    status_value: str | None = Query(default=None, alias="status"),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(
        require_roles(
            UserRole.SCHOOL_ADMIN,
            UserRole.TEACHER,
        )
    ),
) -> ApiResponse[PageResponse[StudentResponse]]:
    _ = StudentListQuery(
        page=page,
        page_size=page_size,
        grade_id=grade_id,
        class_id=class_id,
        keyword=keyword,
        status=status_value,
    )
    school_id = _require_school_scope(current_user)
    stmt: Select[tuple[StudentProfile]] = select(StudentProfile).where(
        StudentProfile.school_id == school_id,
        StudentProfile.is_deleted.is_(False),
    )

    if current_user.role == UserRole.TEACHER:
        class_ids = _teacher_accessible_class_ids(session, current_user)
        if not class_ids:
            return ApiResponse.ok(PageResponse(items=[], page=page, page_size=page_size, total=0))
        stmt = stmt.where(StudentProfile.class_id.in_(class_ids))

    if grade_id is not None:
        stmt = stmt.where(StudentProfile.grade_id == grade_id)
    if class_id is not None:
        stmt = stmt.where(StudentProfile.class_id == class_id)
    if keyword:
        like_value = f"%{keyword}%"
        stmt = stmt.where(
            (StudentProfile.name.like(like_value)) | (StudentProfile.student_no.like(like_value))
        )
    if status_value:
        stmt = stmt.where(StudentProfile.status == status_value)

    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = session.execute(total_stmt).scalar_one()
    students = session.execute(
        stmt.order_by(StudentProfile.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()
    return ApiResponse.ok(
        PageResponse(
            items=[StudentResponse.model_validate(student) for student in students],
            page=page,
            page_size=page_size,
            total=total,
        )
    )


@router.get("/me/profile", response_model=ApiResponse[StudentResponse])
def get_my_profile(
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
) -> ApiResponse[StudentResponse]:
    stmt = select(StudentProfile).where(
        StudentProfile.user_id == current_user.id,
        StudentProfile.is_deleted.is_(False),
    )
    student = session.execute(stmt).scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return ApiResponse.ok(StudentResponse.model_validate(student))


@router.get("/{student_id}", response_model=ApiResponse[StudentResponse])
def get_student_detail(
    student_id: int,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(
        require_roles(
            UserRole.SCHOOL_ADMIN,
            UserRole.TEACHER,
            UserRole.STUDENT,
        )
    ),
) -> ApiResponse[StudentResponse]:
    student = _get_student_or_404(session, student_id)
    school_id = _require_school_scope(current_user)
    _ensure_student_in_school(student, school_id)

    if current_user.role == UserRole.STUDENT and student.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    if current_user.role == UserRole.TEACHER:
        class_ids = _teacher_accessible_class_ids(session, current_user)
        if student.class_id not in class_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return ApiResponse.ok(StudentResponse.model_validate(student))


@router.put("/{student_id}", response_model=ApiResponse[StudentResponse])
def update_student(
    student_id: int,
    payload: StudentUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[StudentResponse]:
    school_id = _require_school_scope(current_user)
    student = _get_student_or_404(session, student_id)
    _ensure_student_in_school(student, school_id)
    user = session.get(User, student.user_id)
    if user is None or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.grade_id is not None:
        grade = session.get(Grade, payload.grade_id)
        if grade is None or grade.is_deleted or grade.school_id != school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade")
        student.grade_id = payload.grade_id

    if payload.class_id is not None:
        classroom = session.get(Classroom, payload.class_id)
        if classroom is None or classroom.is_deleted or classroom.school_id != school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid class")
        if student.class_id != payload.class_id:
            current_relations = session.execute(
                select(ClassStudent).where(
                    ClassStudent.student_id == student.id,
                    ClassStudent.is_current.is_(True),
                )
            ).scalars().all()
            for relation in current_relations:
                relation.is_current = False
            session.add(
                ClassStudent(
                    school_id=school_id,
                    class_id=payload.class_id,
                    student_id=student.id,
                    is_current=True,
                )
            )
            student.class_id = payload.class_id

    if payload.name is not None:
        student.name = payload.name
        user.name = payload.name
    if payload.gender is not None:
        student.gender = payload.gender
    if payload.phone is not None:
        student.phone = payload.phone
        user.phone = payload.phone
    if payload.status is not None:
        student.status = payload.status
        user.status = payload.status

    session.add_all([student, user])
    session.commit()
    session.refresh(student)
    return ApiResponse.ok(StudentResponse.model_validate(student))


@router.post("/{student_id}/status", response_model=ApiResponse[StudentResponse])
def change_student_status(
    student_id: int,
    payload: StudentStatusUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[StudentResponse]:
    school_id = _require_school_scope(current_user)
    student = _get_student_or_404(session, student_id)
    _ensure_student_in_school(student, school_id)
    user = session.get(User, student.user_id)
    if user is None or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    student.status = payload.status
    user.status = payload.status
    session.add_all([student, user])
    session.commit()
    session.refresh(student)
    return ApiResponse.ok(StudentResponse.model_validate(student))
