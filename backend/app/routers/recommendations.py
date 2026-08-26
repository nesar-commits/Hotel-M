from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.ml import recommender

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/user/{user_id}", response_model=list[schemas.MenuItemOut])
def recommend_for_user(user_id: int, top_n: int = 10, db: Session = Depends(get_db)):
    history = crud.get_order_menu_items_for_user(db, user_id)
    catalog = crud.all_menu_items(db)
    return recommender.recommend_for_user(history, catalog, top_n=top_n)


@router.get("/similar/{menu_item_id}", response_model=list[schemas.MenuItemOut])
def similar_items(menu_item_id: int, top_n: int = 6, db: Session = Depends(get_db)):
    item = crud.get_menu_item(db, menu_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    catalog = crud.list_menu_items(db, item.restaurant_id)
    return recommender.similar_items(menu_item_id, catalog, top_n=top_n)


@router.get("/popular/{restaurant_id}", response_model=list[schemas.MenuItemOut])
def popular_in_restaurant(restaurant_id: int, top_n: int = 10, db: Session = Depends(get_db)):
    catalog = crud.list_menu_items(db, restaurant_id)
    return recommender.popular_items(catalog, top_n=top_n)
