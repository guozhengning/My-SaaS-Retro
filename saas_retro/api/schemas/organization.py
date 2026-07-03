from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GradeCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    academic_year: str = Field(min_length=1, max_length=32)
    status: str = Field(default="active", pattern="^(active|inactive)$")


class GradeUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=64)
    academic_year: str | None = Field(default=None, min_length=1, max_length=32)
    status: str | None = Field(default=None, pattern="^(active|inactive)$")


class GradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int
    name: str
    academic_year: str
    status: str


class ClassCreateRequest(BaseModel):
    grade_id: int
    name: str = Field(min_length=1, max_length=64)
    head_teacher_id: int | None = None
    status: str = Field(default="active", pattern="^(active|inactive)$")


class ClassUpdateRequest(BaseModel):
    grade_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=64)
    head_teacher_id: int | None = None
    status: str | None = Field(default=None, pattern="^(active|inactive)$")


class ClassResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int
    grade_id: int
    name: str
    head_teacher_id: int | None
    status: str
