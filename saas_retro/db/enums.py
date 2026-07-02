from __future__ import annotations

from enum import StrEnum


class UserRole(StrEnum):
    PLATFORM_ADMIN = "platform_admin"
    SCHOOL_ADMIN = "school_admin"
    TEACHER = "teacher"
    STUDENT = "student"


class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class WorkflowType(StrEnum):
    LEAVE_REQUEST = "leave_request"
    CERTIFICATE_REQUEST = "certificate_request"


class WorkflowTemplateStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"


class WorkflowNodeType(StrEnum):
    START = "start"
    APPROVAL = "approval"
    ISSUE = "issue"
    END = "end"


class ApproverType(StrEnum):
    HEAD_TEACHER = "head_teacher"
    COURSE_TEACHER = "course_teacher"
    SCHOOL_ADMIN = "school_admin"
    CERTIFICATE_ADMIN = "certificate_admin"


class ActionKey(StrEnum):
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    REVOKE = "revoke"
    RESUBMIT = "resubmit"
    ISSUE = "issue"


class WorkflowInstanceStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"
    ISSUED = "issued"
    COMPLETED = "completed"


class WorkflowTaskStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"
    ISSUED = "issued"


class EvaluationTaskStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class AnonymousMode(StrEnum):
    ANONYMOUS = "anonymous"
    REAL_NAME = "real_name"


class ScoreScaleType(StrEnum):
    FIVE_POINT = "five_point"
    TEN_POINT = "ten_point"
    HUNDRED_POINT = "hundred_point"
    CUSTOM = "custom"


class ScoreType(StrEnum):
    NUMERIC = "numeric"
    GRADE = "grade"
    PASS_FAIL = "pass_fail"


class PublishStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


class ExamStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
