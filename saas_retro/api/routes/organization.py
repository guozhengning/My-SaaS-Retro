from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from saas_retro.api.deps import get_current_user, get_db_session, require_roles
from saas_retro.api.schemas.common import ApiResponse
from saas_retro.api.schemas.organization import (
    ClassCreateRequest,
    ClassResponse,
    ClassUpdateRequest,
    GradeCreateRequest,
    GradeResponse,
    GradeUpdateRequest,
)
from saas_retro.db.enums import UserRole
from saas_retro.db.models.organization import Classroom, Grade, TeacherProfile, User

router = APIRouter(prefix="/api/v1/org", tags=["organization"])


def _school_id(current_user: User) -> int:
    if current_user.school_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="School scope required")
    return current_user.school_id


@router.post("/grades", response_model=ApiResponse[GradeResponse])
def create_grade(
    payload: GradeCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[GradeResponse]:
    school_id = _school_id(current_user)
    existing = session.execute(
        select(Grade).where(
            Grade.school_id == school_id,
            Grade.name == payload.name,
            Grade.academic_year == payload.academic_year,
            Grade.is_deleted.is_(False),
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Grade already exists")

    grade = Grade(
        school_id=school_id,
        name=payload.name,
        academic_year=payload.academic_year,
        status=payload.status,
    )
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return ApiResponse.ok(GradeResponse.model_validate(grade))


@router.get("/grades", response_model=ApiResponse[list[GradeResponse]])
def list_grades(
    status_value: str | None = Query(default=None, alias="status"),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN, UserRole.TEACHER)),
) -> ApiResponse[list[GradeResponse]]:
    school_id = _school_id(current_user)
    stmt = select(Grade).where(Grade.school_id == school_id, Grade.is_deleted.is_(False))
    if status_value:
        stmt = stmt.where(Grade.status == status_value)
    grades = session.execute(stmt.order_by(Grade.id.desc())).scalars().all()
    return ApiResponse.ok([GradeResponse.model_validate(grade) for grade in grades])


@router.put("/grades/{grade_id}", response_model=ApiResponse[GradeResponse])
def update_grade(
    grade_id: int,
    payload: GradeUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[GradeResponse]:
    school_id = _school_id(current_user)
    grade = session.get(Grade, grade_id)
    if grade is None or grade.is_deleted or grade.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")

    if payload.name is not None:
        grade.name = payload.name
    if payload.academic_year is not None:
        grade.academic_year = payload.academic_year
    if payload.status is not None:
        grade.status = payload.status

    session.add(grade)
    session.commit()
    session.refresh(grade)
    return ApiResponse.ok(GradeResponse.model_validate(grade))


@router.post("/classes", response_model=ApiResponse[ClassResponse])
def create_class(
    payload: ClassCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[ClassResponse]:
    school_id = _school_id(current_user)
    grade = session.get(Grade, payload.grade_id)
    if grade is None or grade.is_deleted or grade.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade")

    if payload.head_teacher_id is not None:
        teacher = session.get(TeacherProfile, payload.head_teacher_id)
        if teacher is None or teacher.is_deleted or teacher.school_id != school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid teacher")

    existing = session.execute(
        select(Classroom).where(
            Classroom.school_id == school_id,
            Classroom.grade_id == payload.grade_id,
            Classroom.name == payload.name,
            Classroom.is_deleted.is_(False),
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Class already exists")

    classroom = Classroom(
        school_id=school_id,
        grade_id=payload.grade_id,
        name=payload.name,
        head_teacher_id=payload.head_teacher_id,
        status=payload.status,
    )
    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return ApiResponse.ok(ClassResponse.model_validate(classroom))


@router.get("/classes", response_model=ApiResponse[list[ClassResponse]])
def list_classes(
    grade_id: int | None = Query(default=None),
    status_value: str | None = Query(default=None, alias="status"),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN, UserRole.TEACHER)),
) -> ApiResponse[list[ClassResponse]]:
    school_id = _school_id(current_user)
    stmt = select(Classroom).where(Classroom.school_id == school_id, Classroom.is_deleted.is_(False))
    if grade_id is not None:
        stmt = stmt.where(Classroom.grade_id == grade_id)
    if status_value:
        stmt = stmt.where(Classroom.status == status_value)
    classrooms = session.execute(stmt.order_by(Classroom.id.desc())).scalars().all()
    return ApiResponse.ok([ClassResponse.model_validate(classroom) for classroom in classrooms])


@router.put("/classes/{class_id}", response_model=ApiResponse[ClassResponse])
def update_class(
    class_id: int,
    payload: ClassUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.SCHOOL_ADMIN)),
) -> ApiResponse[ClassResponse]:
    school_id = _school_id(current_user)
    classroom = session.get(Classroom, class_id)
    if classroom is None or classroom.is_deleted or classroom.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    if payload.grade_id is not None:
        grade = session.get(Grade, payload.grade_id)
        if grade is None or grade.is_deleted or grade.school_id != school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade")
        classroom.grade_id = payload.grade_id
    if payload.head_teacher_id is not None:
        teacher = session.get(TeacherProfile, payload.head_teacher_id)
        if teacher is None or teacher.is_deleted or teacher.school_id != school_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid teacher")
        classroom.head_teacher_id = payload.head_teacher_id
    if payload.name is not None:
        classroom.name = payload.name
    if payload.status is not None:
        classroom.status = payload.status

    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return ApiResponse.ok(ClassResponse.model_validate(classroom))
