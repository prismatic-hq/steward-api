import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from steward_api.db import get_session
from steward_api.models import WorkOrder
from steward_api.schemas import WorkOrderCreate, WorkOrderRead, WorkOrderUpdate

router = APIRouter(prefix="/work-orders", tags=["work-orders"])
SessionDep = Annotated[Session, Depends(get_session)]


def _get_or_404(session: Session, work_order_id: uuid.UUID) -> WorkOrder:
    work_order = session.get(WorkOrder, work_order_id)
    if work_order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"work order {work_order_id} not found")
    return work_order


@router.post("", response_model=WorkOrderRead, status_code=status.HTTP_201_CREATED)
def create_work_order(payload: WorkOrderCreate, session: SessionDep) -> WorkOrder:
    work_order = WorkOrder(**payload.model_dump())
    session.add(work_order)
    session.commit()
    session.refresh(work_order)
    return work_order


@router.get("", response_model=list[WorkOrderRead])
def list_work_orders(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[WorkOrder]:
    query = (
        select(WorkOrder).order_by(WorkOrder.created_at, WorkOrder.id).limit(limit).offset(offset)
    )
    return list(session.scalars(query))


@router.get("/{work_order_id}", response_model=WorkOrderRead)
def get_work_order(work_order_id: uuid.UUID, session: SessionDep) -> WorkOrder:
    return _get_or_404(session, work_order_id)


@router.patch("/{work_order_id}", response_model=WorkOrderRead)
def update_work_order(
    work_order_id: uuid.UUID, payload: WorkOrderUpdate, session: SessionDep
) -> WorkOrder:
    work_order = _get_or_404(session, work_order_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(work_order, field, value)
    session.commit()
    session.refresh(work_order)
    return work_order


@router.delete("/{work_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_order(work_order_id: uuid.UUID, session: SessionDep) -> None:
    session.delete(_get_or_404(session, work_order_id))
    session.commit()
