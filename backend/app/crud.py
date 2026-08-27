from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.geo import haversine_km

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Restaurants ----------
def list_restaurants(db: Session, city: str | None = None, search: str | None = None):
    query = db.query(models.Restaurant)
    if city:
        query = query.filter(models.Restaurant.city.ilike(f"%{city}%"))
    if search:
        query = query.filter(models.Restaurant.name.ilike(f"%{search}%"))
    return query.order_by(models.Restaurant.rating.desc()).all()


def get_restaurant(db: Session, restaurant_id: int):
    return (
        db.query(models.Restaurant)
        .options(
            joinedload(models.Restaurant.categories),
            joinedload(models.Restaurant.menu_items),
        )
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )


def list_restaurants_near(db: Session, lat: float, lng: float, limit: int = 20):
    restaurants = db.query(models.Restaurant).all()
    with_distance = [
        (r, haversine_km(lat, lng, r.latitude, r.longitude)) for r in restaurants
    ]
    with_distance.sort(key=lambda pair: pair[1])
    results = []
    for restaurant, distance in with_distance[:limit]:
        data = schemas.RestaurantOut.model_validate(restaurant).model_dump()
        results.append(schemas.RestaurantWithDistanceOut(**data, distance_km=round(distance, 1)))
    return results


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# ---------- Categories ----------
def create_category(db: Session, restaurant_id: int, category: schemas.CategoryCreate):
    db_category = models.Category(restaurant_id=restaurant_id, **category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ---------- Menu items ----------
def list_menu_items(db: Session, restaurant_id: int, category_id: int | None = None,
                     is_veg: bool | None = None, search: str | None = None):
    query = db.query(models.MenuItem).filter(
        models.MenuItem.restaurant_id == restaurant_id
    )
    if category_id is not None:
        query = query.filter(models.MenuItem.category_id == category_id)
    if is_veg is not None:
        query = query.filter(models.MenuItem.is_veg == is_veg)
    if search:
        query = query.filter(models.MenuItem.name.ilike(f"%{search}%"))
    return query.all()


def create_menu_item(db: Session, restaurant_id: int, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(restaurant_id=restaurant_id, **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_menu_item(db: Session, menu_item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()


def all_menu_items(db: Session):
    return db.query(models.MenuItem).filter(models.MenuItem.is_available.is_(True)).all()


# ---------- Users ----------
def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# ---------- Orders ----------
def create_order(db: Session, order: schemas.OrderCreate):
    if not db.query(models.User).filter(models.User.id == order.user_id).first():
        raise ValueError(f"User {order.user_id} not found")
    if not db.query(models.Restaurant).filter(models.Restaurant.id == order.restaurant_id).first():
        raise ValueError(f"Restaurant {order.restaurant_id} not found")

    total = 0.0
    order_items = []
    for item in order.items:
        menu_item = get_menu_item(db, item.menu_item_id)
        if not menu_item:
            raise ValueError(f"Menu item {item.menu_item_id} not found")
        line_total = menu_item.price * item.quantity
        total += line_total
        order_items.append(
            models.OrderItem(
                menu_item_id=menu_item.id,
                quantity=item.quantity,
                price=menu_item.price,
            )
        )

    db_order = models.Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        total_amount=total,
        items=order_items,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def list_orders_for_user(db: Session, user_id: int):
    return (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .all()
    )


def get_order_menu_items_for_user(db: Session, user_id: int) -> list[models.MenuItem]:
    orders = list_orders_for_user(db, user_id)
    menu_item_ids = {oi.menu_item_id for order in orders for oi in order.items}
    if not menu_item_ids:
        return []
    return (
        db.query(models.MenuItem)
        .filter(models.MenuItem.id.in_(menu_item_ids))
        .all()
    )
