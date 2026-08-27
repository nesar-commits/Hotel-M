from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[schemas.RestaurantOut])
def list_restaurants(
    city: str | None = None, search: str | None = None, db: Session = Depends(get_db)
):
    return crud.list_restaurants(db, city=city, search=search)


@router.post("", response_model=schemas.RestaurantOut, status_code=201)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db, restaurant)


@router.get("/nearby", response_model=list[schemas.RestaurantWithDistanceOut])
def list_nearby_restaurants(
    lat: float, lng: float, limit: int = 20, db: Session = Depends(get_db)
):
    return crud.list_restaurants_near(db, lat=lat, lng=lng, limit=limit)


@router.get("/{restaurant_id}", response_model=schemas.RestaurantDetailOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.post("/{restaurant_id}/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(
    restaurant_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_category(db, restaurant_id, category)
