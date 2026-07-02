from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import AuditUserMixin, Base, SoftDeleteMixin, TimestampMixin
from ..enums import (
    ActionKey,
    ApproverType,
    Status,
    WorkflowInstanceStatus,
    WorkflowNodeType,
    WorkflowTaskStatus,
    WorkflowTemplateStatus,
    WorkflowType,
)


class WorkflowTemplate(TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "workflow_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    workflow_type_key: Mapped[WorkflowType] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[WorkflowTemplateStatus] = mapped_column(
        String(16), nullable=False, default=WorkflowTemplateStatus.DRAFT
    )
    version: Mapped[int] = mapped_column(nullable=False, default=1)

    nodes: Mapped[list["WorkflowTemplateNode"]] = relationship(back_populates="template")
    leave_requests: Mapped[list["LeaveRequest"]] = relationship(back_populates="workflow_template")
    certificate_requests: Mapped[list["CertificateRequest"]] = relationship(
        back_populates="workflow_template"
    )


class WorkflowTemplateNode(TimestampMixin, Base):
    __tablename__ = "workflow_template_nodes"
    __table_args__ = (
        UniqueConstraint("template_id", "node_key", name="uk_workflow_template_nodes_template_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    template_id: Mapped[int] = mapped_column(ForeignKey("workflow_templates.id"), nullable=False)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    node_name: Mapped[str] = mapped_column(String(64), nullable=False)
    node_type_key: Mapped[WorkflowNodeType] = mapped_column(String(32), nullable=False)
    approver_type_key: Mapped[ApproverType | None] = mapped_column(String(32))
    sort_order: Mapped[int] = mapped_column(nullable=False)

    template: Mapped[WorkflowTemplate] = relationship(back_populates="nodes")


class WorkflowInstance(TimestampMixin, Base):
    __tablename__ = "workflow_instances"
    __table_args__ = (
        UniqueConstraint("business_type", "business_id", name="uk_workflow_instances_business"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    workflow_type_key: Mapped[WorkflowType] = mapped_column(String(64), nullable=False)
    template_id: Mapped[int] = mapped_column(ForeignKey("workflow_templates.id"), nullable=False)
    template_version: Mapped[int] = mapped_column(nullable=False)
    business_type: Mapped[str] = mapped_column(String(64), nullable=False)
    business_id: Mapped[int] = mapped_column(nullable=False)
    current_node_key: Mapped[str | None] = mapped_column(String(64))
    current_node_name: Mapped[str | None] = mapped_column(String(64))
    instance_status: Mapped[WorkflowInstanceStatus] = mapped_column(String(32), nullable=False)
    started_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime | None]

    instance_nodes: Mapped[list["WorkflowInstanceNode"]] = relationship(back_populates="instance")
    tasks: Mapped[list["WorkflowTask"]] = relationship(back_populates="instance")
    action_logs: Mapped[list["WorkflowActionLog"]] = relationship(back_populates="instance")
    leave_request: Mapped["LeaveRequest | None"] = relationship(back_populates="workflow_instance")
    certificate_request: Mapped["CertificateRequest | None"] = relationship(
        back_populates="workflow_instance"
    )


class WorkflowInstanceNode(TimestampMixin, Base):
    __tablename__ = "workflow_instance_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    instance_id: Mapped[int] = mapped_column(ForeignKey("workflow_instances.id"), nullable=False)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    node_name: Mapped[str] = mapped_column(String(64), nullable=False)
    node_type_key: Mapped[WorkflowNodeType] = mapped_column(String(32), nullable=False)
    approver_type_key: Mapped[ApproverType | None] = mapped_column(String(32))
    sort_order: Mapped[int] = mapped_column(nullable=False)
    node_status: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]

    instance: Mapped[WorkflowInstance] = relationship(back_populates="instance_nodes")


class WorkflowTask(TimestampMixin, Base):
    __tablename__ = "workflow_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    instance_id: Mapped[int] = mapped_column(ForeignKey("workflow_instances.id"), nullable=False)
    business_type: Mapped[str] = mapped_column(String(64), nullable=False)
    business_id: Mapped[int] = mapped_column(nullable=False)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    node_name: Mapped[str] = mapped_column(String(64), nullable=False)
    approver_type_key: Mapped[ApproverType] = mapped_column(String(32), nullable=False)
    assignee_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    task_status: Mapped[WorkflowTaskStatus] = mapped_column(String(32), nullable=False)
    actioned_at: Mapped[datetime | None]
    comment: Mapped[str | None] = mapped_column(String(255))

    instance: Mapped[WorkflowInstance] = relationship(back_populates="tasks")


class WorkflowActionLog(Base):
    __tablename__ = "workflow_action_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    instance_id: Mapped[int] = mapped_column(ForeignKey("workflow_instances.id"), nullable=False)
    business_type: Mapped[str] = mapped_column(String(64), nullable=False)
    business_id: Mapped[int] = mapped_column(nullable=False)
    node_key: Mapped[str | None] = mapped_column(String(64))
    action_key: Mapped[ActionKey] = mapped_column(String(32), nullable=False)
    operator_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    operator_role: Mapped[str] = mapped_column(String(32), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime]

    instance: Mapped[WorkflowInstance] = relationship(back_populates="action_logs")


class LeaveRequest(TimestampMixin, Base):
    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    workflow_template_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_templates.id"), nullable=False
    )
    workflow_instance_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_instances.id"))
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    instance_status: Mapped[WorkflowInstanceStatus] = mapped_column(String(32), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    workflow_template: Mapped[WorkflowTemplate] = relationship(back_populates="leave_requests")
    workflow_instance: Mapped[WorkflowInstance | None] = relationship(back_populates="leave_request")


class CertificateType(TimestampMixin, Base):
    __tablename__ = "certificate_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[Status] = mapped_column(String(16), nullable=False, default=Status.ACTIVE)

    requests: Mapped[list["CertificateRequest"]] = relationship(back_populates="certificate_type")


class CertificateRequest(TimestampMixin, Base):
    __tablename__ = "certificate_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    certificate_type_id: Mapped[int] = mapped_column(
        ForeignKey("certificate_types.id"), nullable=False
    )
    workflow_template_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_templates.id"), nullable=False
    )
    workflow_instance_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_instances.id"))
    purpose: Mapped[str] = mapped_column(String(255), nullable=False)
    copies: Mapped[int] = mapped_column(nullable=False, default=1)
    instance_status: Mapped[WorkflowInstanceStatus] = mapped_column(String(32), nullable=False)
    download_url: Mapped[str | None] = mapped_column(String(255))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    certificate_type: Mapped[CertificateType] = relationship(back_populates="requests")
    workflow_template: Mapped[WorkflowTemplate] = relationship(back_populates="certificate_requests")
    workflow_instance: Mapped[WorkflowInstance | None] = relationship(
        back_populates="certificate_request"
    )
