from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Category ----------
class CategoryBase(BaseModel):
    name: str
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_id: int


# ---------- Menu Item ----------
class MenuItemBase(BaseModel):
    name: str
    description: str = ""
    price: float
    is_veg: bool = True
    is_available: bool = True
    image_url: str = ""
    rating: float = 0.0
    tags: str = ""


class MenuItemCreate(MenuItemBase):
    category_id: int


class MenuItemOut(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_id: int
    category_id: int


# ---------- Restaurant ----------
class RestaurantBase(BaseModel):
    name: str
    description: str = ""
    cuisine_type: str = ""
    city: str = ""
    address: str = ""
    rating: float = 0.0
    cost_for_two: int = 0
    image_url: str = ""
    is_open: bool = True
    latitude: float = 0.0
    longitude: float = 0.0


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantOut(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class RestaurantDetailOut(RestaurantOut):
    categories: list[CategoryOut] = []
    menu_items: list[MenuItemOut] = []


class RestaurantWithDistanceOut(RestaurantOut):
    distance_km: float


# ---------- User ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr


# ---------- Order ----------
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    menu_item_id: int
    quantity: int
    price: float


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    restaurant_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut] = []
