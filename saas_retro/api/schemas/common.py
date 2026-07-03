from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    code: int
    message: str
    data: T

    @classmethod
    def ok(cls, data: T, message: str = "成功") -> "ApiResponse[T]":
        return cls(code=0, message=message, data=data)
