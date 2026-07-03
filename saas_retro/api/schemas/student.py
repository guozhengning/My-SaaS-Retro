from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StudentCreateRequest(BaseModel):
    student_no: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    gender: str | None = None
    grade_id: int
    class_id: int
    phone: str | None = None
    password: str = Field(min_length=6, max_length=128)
    status: str = "active"


class StudentUpdateRequest(BaseModel):
    name: str | None = None
    gender: str | None = None
    grade_id: int | None = None
    class_id: int | None = None
    phone: str | None = None
    status: str | None = None


class StudentStatusUpdateRequest(BaseModel):
    status: str = Field(pattern="^(active|inactive)$")


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int
    user_id: int
    student_no: str
    name: str
    gender: str | None
    grade_id: int
    class_id: int
    phone: str | None
    status: str


class StudentListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    grade_id: int | None = None
    class_id: int | None = None
    keyword: str | None = None
    status: str | None = None
