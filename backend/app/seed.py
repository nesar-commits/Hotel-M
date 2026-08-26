"""Seeds the database with sample restaurants and menu items for local dev.

Run with: python -m app.seed
"""

from app import models
from app.crud import pwd_context
from app.database import Base, SessionLocal, engine

def _img(photo_id: str) -> str:
    return f"https://images.unsplash.com/{photo_id}?w=400"


RESTAURANTS = [
    {
        "name": "Spice Route Kitchen",
        "description": "Modern North Indian comfort food with a tandoori soul.",
        "cuisine_type": "North Indian, Mughlai",
        "city": "Mumbai",
        "address": "12 MG Road, Mumbai",
        "rating": 4.4,
        "cost_for_two": 700,
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "categories": ["Starters", "Main Course", "Breads", "Desserts", "Beverages"],
        "items": [
            ("Paneer Tikka", "Char-grilled cottage cheese marinated in spiced yogurt", 220, True, "Starters", "grilled,tandoori,paneer", _img("photo-1567188040759-fb8a883dc6d8")),
            ("Chicken Seekh Kebab", "Minced chicken skewers with garam masala", 260, False, "Starters", "grilled,tandoori,chicken", _img("photo-1633945274405-b6c8069047b0")),
            ("Butter Chicken", "Creamy tomato-based curry with tandoori chicken", 320, False, "Main Course", "curry,creamy,chicken,north indian", _img("photo-1603894584373-5ac82b2ae398")),
            ("Dal Makhani", "Slow-cooked black lentils with butter and cream", 240, True, "Main Course", "curry,creamy,lentils,north indian", _img("photo-1546833999-b9f581a1996d")),
            ("Palak Paneer", "Cottage cheese in a spiced spinach gravy", 260, True, "Main Course", "curry,spinach,paneer", _img("photo-1626200419199-391ae4be7a41")),
            ("Butter Naan", "Leavened bread baked in a tandoor with butter", 60, True, "Breads", "bread,tandoori", _img("photo-1565557623262-b51c2513a641")),
            ("Gulab Jamun", "Milk dumplings soaked in rose-cardamom syrup", 120, True, "Desserts", "sweet,dessert,milk", _img("photo-1517244683847-7456b63c5969")),
            ("Masala Chaas", "Spiced buttermilk with curry leaves and cumin", 80, True, "Beverages", "drink,cooling,yogurt", _img("photo-1544145945-f90425340c7e")),
        ],
    },
    {
        "name": "Little Italy Pizzeria",
        "description": "Wood-fired pizzas and fresh handmade pasta.",
        "cuisine_type": "Italian, Pizza",
        "city": "Mumbai",
        "address": "45 Linking Road, Bandra, Mumbai",
        "rating": 4.6,
        "cost_for_two": 900,
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
        "categories": ["Starters", "Pizza", "Pasta", "Desserts", "Beverages"],
        "items": [
            ("Bruschetta", "Toasted bread with tomato, basil and olive oil", 210, True, "Starters", "italian,bread,tomato", _img("photo-1572695157366-5e585ab2b69f")),
            ("Garlic Bread with Cheese", "Baked garlic bread topped with mozzarella", 190, True, "Starters", "italian,bread,cheese", _img("photo-1548940740-204726a19be3")),
            ("Margherita Pizza", "Classic tomato, mozzarella and fresh basil", 380, True, "Pizza", "pizza,cheese,tomato,italian", _img("photo-1595854341625-f33ee10dbf94")),
            ("Pepperoni Pizza", "Loaded with spicy pepperoni and mozzarella", 450, False, "Pizza", "pizza,cheese,spicy,italian", _img("photo-1594007654729-407eedc4be65")),
            ("Farmhouse Pizza", "Onion, capsicum, mushroom, tomato and corn", 420, True, "Pizza", "pizza,veggie,italian", _img("photo-1513104890138-7c749659a591")),
            ("Penne Alfredo", "Creamy white sauce pasta with herbs", 340, True, "Pasta", "pasta,creamy,italian", _img("photo-1481931098730-318b6f776db0")),
            ("Spaghetti Arrabbiata", "Spicy tomato and garlic pasta", 320, True, "Pasta", "pasta,spicy,tomato,italian", _img("photo-1551183053-bf91a1d81141")),
            ("Tiramisu", "Coffee-soaked layers with mascarpone cream", 220, True, "Desserts", "sweet,dessert,coffee,italian", _img("photo-1571877227200-a0d98ea607e9")),
            ("Italian Soda", "Sparkling water with fruit syrup", 150, True, "Beverages", "drink,cold,italian", _img("photo-1621263764928-df1444c5e859")),
        ],
    },
    {
        "name": "Dragon Wok",
        "description": "Indo-Chinese and Pan-Asian favourites, wok-tossed fresh.",
        "cuisine_type": "Chinese, Asian",
        "city": "Bengaluru",
        "address": "8 Indiranagar 100ft Road, Bengaluru",
        "rating": 4.2,
        "cost_for_two": 600,
        "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
        "categories": ["Starters", "Main Course", "Rice & Noodles", "Beverages"],
        "items": [
            ("Veg Spring Rolls", "Crispy rolls stuffed with cabbage and carrots", 180, True, "Starters", "chinese,fried,veggie", _img("photo-1563245372-f21724e3856d")),
            ("Chilli Chicken", "Wok-tossed chicken in spicy soy-chilli sauce", 280, False, "Starters", "chinese,spicy,chicken", _img("photo-1525755662778-989d0524087e")),
            ("Manchurian (Veg)", "Fried vegetable balls in tangy Manchurian sauce", 220, True, "Main Course", "chinese,spicy,veggie", _img("photo-1585032226651-759b368d7246")),
            ("Kung Pao Chicken", "Stir-fried chicken with peanuts and chilli", 300, False, "Main Course", "chinese,spicy,chicken,nuts", _img("photo-1617093727343-374698b1b08d")),
            ("Veg Hakka Noodles", "Stir-fried noodles with fresh vegetables", 210, True, "Rice & Noodles", "chinese,noodles,veggie", _img("photo-1583032015879-e5022cb87c3b")),
            ("Egg Fried Rice", "Classic wok-fried rice with egg and spring onion", 200, False, "Rice & Noodles", "chinese,rice,egg", _img("photo-1512058564366-18510be2db19")),
            ("Iced Lemon Tea", "Chilled black tea with fresh lemon", 110, True, "Beverages", "drink,cold,tea", _img("photo-1499638673689-79a0b5115d87")),
        ],
    },
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Restaurant).first():
            print("Database already has data — skipping seed.")
            return

        db.add(
            models.User(
                name="Demo User",
                email="demo@tastyhub.dev",
                hashed_password=pwd_context.hash("demo1234"),
            )
        )
        db.flush()

        for r in RESTAURANTS:
            restaurant = models.Restaurant(
                name=r["name"],
                description=r["description"],
                cuisine_type=r["cuisine_type"],
                city=r["city"],
                address=r["address"],
                rating=r["rating"],
                cost_for_two=r["cost_for_two"],
                image_url=r["image_url"],
            )
            db.add(restaurant)
            db.flush()

            category_map = {}
            for idx, cat_name in enumerate(r["categories"]):
                category = models.Category(
                    restaurant_id=restaurant.id, name=cat_name, sort_order=idx
                )
                db.add(category)
                db.flush()
                category_map[cat_name] = category.id

            for name, desc, price, is_veg, cat_name, tags, image_url in r["items"]:
                db.add(
                    models.MenuItem(
                        restaurant_id=restaurant.id,
                        category_id=category_map[cat_name],
                        name=name,
                        description=desc,
                        price=price,
                        is_veg=is_veg,
                        rating=round(3.8 + (hash(name) % 12) / 10, 1),
                        image_url=image_url,
                        tags=tags,
                    )
                )

        db.commit()
        print("Seeded database with sample restaurants and menu items.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
