from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import get_current_staff_user, get_current_user
from app.database import get_db
from app.order_status import is_valid_status, next_status

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=schemas.OrderOut, status_code=201)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        return crud.create_order(db, current_user.id, order)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/me", response_model=list[schemas.OrderOut])
def list_my_orders(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return crud.list_orders_for_user(db, current_user.id)


@router.get("/kitchen", response_model=list[schemas.OrderOut])
def list_kitchen_orders(
    restaurant_id: int | None = None,
    db: Session = Depends(get_db),
    _staff: models.User = Depends(get_current_staff_user),
):
    return crud.list_orders_for_restaurant(db, restaurant_id=restaurant_id)


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(status_code=403, detail="Not your order")
    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(
    order_id: int,
    payload: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    _staff: models.User = Depends(get_current_staff_user),
):
    if not is_valid_status(payload.status):
        raise HTTPException(status_code=422, detail=f"Invalid status: {payload.status}")
    try:
        return crud.update_order_status(db, order_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{order_id}/advance", response_model=schemas.OrderOut)
def advance_order_status(
    order_id: int,
    db: Session = Depends(get_db),
    _staff: models.User = Depends(get_current_staff_user),
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    upcoming = next_status(order.status)
    if not upcoming:
        raise HTTPException(status_code=400, detail=f"Order is already '{order.status}'")
    return crud.update_order_status(db, order_id, upcoming)
