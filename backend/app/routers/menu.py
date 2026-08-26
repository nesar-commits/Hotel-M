from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/restaurants/{restaurant_id}/menu", tags=["menu"])


@router.get("", response_model=list[schemas.MenuItemOut])
def list_menu_items(
    restaurant_id: int,
    category_id: int | None = None,
    is_veg: bool | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_menu_items(
        db, restaurant_id, category_id=category_id, is_veg=is_veg, search=search
    )


@router.post("", response_model=schemas.MenuItemOut, status_code=201)
def create_menu_item(
    restaurant_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)
):
    return crud.create_menu_item(db, restaurant_id, item)
