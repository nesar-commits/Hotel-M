"""Generates a large batch of demo restaurants for local/dev seeding.

Real restaurant chains and menus aren't available to seed from, so this
procedurally builds plausible restaurants: real Indian city coordinates (for
the geolocation "nearby" feature), one of a handful of cuisine profiles (each
built from verified-loading photos and genuine dish names), and randomized
price/rating variation so the catalog isn't visibly repetitive.
"""

import random

from app import models
from app.data.city_coordinates import CITY_COORDINATES
from app.data.food_images import HERO_IMAGES

CDN = "https://images.unsplash.com/{}?w=400"
CDN_HERO = "https://images.unsplash.com/{}?w=800"


def _img(photo_id: str) -> str:
    return CDN.format(photo_id)


CUISINE_PROFILES = [
    {
        "label": "North Indian, Mughlai",
        "categories": ["Starters", "Main Course", "Breads", "Desserts", "Beverages"],
        "dishes": [
            ("Paneer Tikka", "Char-grilled cottage cheese marinated in spiced yogurt", 220, True, "Starters", "grilled,tandoori,paneer", "photo-1567188040759-fb8a883dc6d8"),
            ("Chicken Seekh Kebab", "Minced chicken skewers with garam masala", 260, False, "Starters", "grilled,tandoori,chicken", "photo-1633945274405-b6c8069047b0"),
            ("Butter Chicken", "Creamy tomato-based curry with tandoori chicken", 320, False, "Main Course", "curry,creamy,chicken,north indian", "photo-1603894584373-5ac82b2ae398"),
            ("Dal Makhani", "Slow-cooked black lentils with butter and cream", 240, True, "Main Course", "curry,creamy,lentils,north indian", "photo-1546833999-b9f581a1996d"),
            ("Palak Paneer", "Cottage cheese in a spiced spinach gravy", 260, True, "Main Course", "curry,spinach,paneer", "photo-1626200419199-391ae4be7a41"),
            ("Butter Naan", "Leavened bread baked in a tandoor with butter", 60, True, "Breads", "bread,tandoori", "photo-1565557623262-b51c2513a641"),
            ("Gulab Jamun", "Milk dumplings soaked in rose-cardamom syrup", 120, True, "Desserts", "sweet,dessert,milk", "photo-1517244683847-7456b63c5969"),
            ("Masala Chaas", "Spiced buttermilk with curry leaves and cumin", 80, True, "Beverages", "drink,cooling,yogurt", "photo-1544145945-f90425340c7e"),
        ],
    },
    {
        "label": "Italian, Pizza",
        "categories": ["Starters", "Pizza", "Pasta", "Desserts", "Beverages"],
        "dishes": [
            ("Bruschetta", "Toasted bread with tomato, basil and olive oil", 210, True, "Starters", "italian,bread,tomato", "photo-1572695157366-5e585ab2b69f"),
            ("Garlic Bread with Cheese", "Baked garlic bread topped with mozzarella", 190, True, "Starters", "italian,bread,cheese", "photo-1548940740-204726a19be3"),
            ("Margherita Pizza", "Classic tomato, mozzarella and fresh basil", 380, True, "Pizza", "pizza,cheese,tomato,italian", "photo-1595854341625-f33ee10dbf94"),
            ("Pepperoni Pizza", "Loaded with spicy pepperoni and mozzarella", 450, False, "Pizza", "pizza,cheese,spicy,italian", "photo-1594007654729-407eedc4be65"),
            ("Farmhouse Pizza", "Onion, capsicum, mushroom, tomato and corn", 420, True, "Pizza", "pizza,veggie,italian", "photo-1513104890138-7c749659a591"),
            ("Penne Alfredo", "Creamy white sauce pasta with herbs", 340, True, "Pasta", "pasta,creamy,italian", "photo-1481931098730-318b6f776db0"),
            ("Spaghetti Arrabbiata", "Spicy tomato and garlic pasta", 320, True, "Pasta", "pasta,spicy,tomato,italian", "photo-1551183053-bf91a1d81141"),
            ("Tiramisu", "Coffee-soaked layers with mascarpone cream", 220, True, "Desserts", "sweet,dessert,coffee,italian", "photo-1571877227200-a0d98ea607e9"),
            ("Italian Soda", "Sparkling water with fruit syrup", 150, True, "Beverages", "drink,cold,italian", "photo-1621263764928-df1444c5e859"),
        ],
    },
    {
        "label": "Chinese, Asian",
        "categories": ["Starters", "Main Course", "Rice & Noodles", "Beverages"],
        "dishes": [
            ("Veg Spring Rolls", "Crispy rolls stuffed with cabbage and carrots", 180, True, "Starters", "chinese,fried,veggie", "photo-1563245372-f21724e3856d"),
            ("Chilli Chicken", "Wok-tossed chicken in spicy soy-chilli sauce", 280, False, "Starters", "chinese,spicy,chicken", "photo-1525755662778-989d0524087e"),
            ("Manchurian (Veg)", "Fried vegetable balls in tangy Manchurian sauce", 220, True, "Main Course", "chinese,spicy,veggie", "photo-1585032226651-759b368d7246"),
            ("Kung Pao Chicken", "Stir-fried chicken with peanuts and chilli", 300, False, "Main Course", "chinese,spicy,chicken,nuts", "photo-1617093727343-374698b1b08d"),
            ("Veg Hakka Noodles", "Stir-fried noodles with fresh vegetables", 210, True, "Rice & Noodles", "chinese,noodles,veggie", "photo-1583032015879-e5022cb87c3b"),
            ("Egg Fried Rice", "Classic wok-fried rice with egg and spring onion", 200, False, "Rice & Noodles", "chinese,rice,egg", "photo-1512058564366-18510be2db19"),
            ("Iced Lemon Tea", "Chilled black tea with fresh lemon", 110, True, "Beverages", "drink,cold,tea", "photo-1499638673689-79a0b5115d87"),
        ],
    },
    {
        "label": "Bakery, Cafe",
        "categories": ["Bakes", "Snacks", "Desserts", "Beverages"],
        "dishes": [
            ("Cinnamon Rolls", "Soft baked rolls swirled with cinnamon sugar", 140, True, "Bakes", "bakery,sweet,breakfast", "photo-1509365465985-25d11c17e812"),
            ("Pav Bhaji", "Spiced mashed vegetable curry with buttered pav", 160, True, "Snacks", "street food,spicy", "photo-1587314168485-3236d6710814"),
            ("Assorted Samosas", "Crispy pastry parcels with spiced potato filling", 90, True, "Snacks", "street food,fried,snack", "photo-1601050690597-df0568f70950"),
            ("Tiramisu Slice", "Coffee-soaked layers with mascarpone cream", 220, True, "Desserts", "sweet,dessert,coffee", "photo-1571877227200-a0d98ea607e9"),
            ("Garden Salad Bowl", "Fresh greens, corn, tomato and grilled paneer", 180, True, "Snacks", "healthy,salad,light", "photo-1546069901-ba9599a7e63c"),
            ("Iced Lemonade", "Freshly squeezed lemonade over ice with mint", 130, True, "Beverages", "drink,cold,citrus", "photo-1621263764928-df1444c5e859"),
            ("House Mocktail", "A refreshing house-blend fruit mocktail", 170, True, "Beverages", "drink,mocktail", "photo-1437418747212-8d9709afab22"),
        ],
    },
    {
        "label": "Multi-Cuisine, Family Restaurant",
        "categories": ["Starters", "Main Course", "Rice & Noodles", "Beverages"],
        "dishes": [
            ("Assorted Samosas", "Crispy pastry parcels with spiced potato filling", 90, True, "Starters", "street food,fried,snack", "photo-1601050690117-94f5f6fa8bd7"),
            ("Chicken Seekh Kebab", "Minced chicken skewers with garam masala", 260, False, "Starters", "grilled,tandoori,chicken", "photo-1633945274405-b6c8069047b0"),
            ("Butter Chicken", "Creamy tomato-based curry with tandoori chicken", 320, False, "Main Course", "curry,creamy,chicken,north indian", "photo-1565557623262-b51c2513a641"),
            ("Chilli Chicken", "Wok-tossed chicken in spicy soy-chilli sauce", 280, False, "Main Course", "chinese,spicy,chicken", "photo-1525755662778-989d0524087e"),
            ("Veg Hakka Noodles", "Stir-fried noodles with fresh vegetables", 210, True, "Rice & Noodles", "chinese,noodles,veggie", "photo-1583032015879-e5022cb87c3b"),
            ("Egg Fried Rice", "Classic wok-fried rice with egg and spring onion", 200, False, "Rice & Noodles", "chinese,rice,egg", "photo-1512058564366-18510be2db19"),
            ("Masala Chaas", "Spiced buttermilk with curry leaves and cumin", 80, True, "Beverages", "drink,cooling,yogurt", "photo-1544145945-f90425340c7e"),
        ],
    },
    {
        "label": "American, Fast Food",
        "categories": ["Burgers", "Sides", "Beverages"],
        "dishes": [
            ("Classic Cheeseburger", "Juicy beef patty with cheddar, lettuce and tomato", 220, False, "Burgers", "burger,fastfood,beef", "photo-1568901346375-23c9450c58cd"),
            ("Double Beef Burger", "Two beef patties stacked with cheese and pickles", 280, False, "Burgers", "burger,fastfood,beef", "photo-1550547660-d9450f859349"),
            ("Crispy Fried Chicken", "Buttermilk-fried chicken with a crunchy coating", 260, False, "Burgers", "fried,chicken,fastfood", "photo-1553163147-622ab57be1c7"),
            ("Buffalo Wings", "Spicy buffalo wings served with ranch dip", 240, False, "Sides", "fried,chicken,spicy", "photo-1567620832903-9fc6debc209f"),
            ("Loaded Fries", "Crispy fries loaded with cheese and toppings", 160, True, "Sides", "fried,snack,cheese", "photo-1573225342350-16731dd9bf3d"),
            ("Chocolate Milkshake", "Thick chocolate shake topped with whipped cream", 180, True, "Beverages", "drink,cold,dessert", "photo-1557142046-c704a3adf364"),
        ],
    },
    {
        "label": "Continental, Steakhouse",
        "categories": ["Starters", "Main Course", "Soups", "Beverages"],
        "dishes": [
            ("Grilled Steak", "Char-grilled steak served with roasted vegetables", 650, False, "Main Course", "steak,grilled,continental", "photo-1432139509613-5c4255815697"),
            ("Herb Roast Chicken", "Whole roasted chicken with herb butter", 480, False, "Main Course", "roast,chicken,continental", "photo-1594221708779-94832f4320d1"),
            ("Pan-Seared Fish", "Pan-seared fish fillet with a citrus glaze", 420, False, "Main Course", "seafood,grilled,continental", "photo-1567337710282-00832b415979"),
            ("Pumpkin Soup", "Creamy roasted pumpkin soup with a swirl of cream", 190, True, "Soups", "soup,creamy,starter", "photo-1476718406336-bb5a9690ee2a"),
            ("Garden Pasta Salad", "Fresh pasta salad with garden vegetables", 220, True, "Starters", "salad,healthy,pasta", "photo-1540189549336-e6e99c3679fe"),
            ("House Mocktail", "A refreshing house-blend fruit mocktail", 170, True, "Beverages", "drink,mocktail", "photo-1437418747212-8d9709afab22"),
        ],
    },
]

ADJECTIVES = [
    "Golden", "Royal", "Spice", "Urban", "Grand", "Classic", "Zaika", "Swad",
    "Tasty", "Sizzling", "Curry", "Tandoor", "Coastal", "Sunrise", "Green",
    "Copper", "Silver", "Vintage", "Modern", "Rustic", "Cozy", "Metro",
    "City", "Star", "Heritage", "Ruby", "Saffron", "Velvet", "Blue", "Red",
    "Amber", "Bombay", "Delhi", "Punjab", "Southern", "Northern", "Prime",
    "Fresh", "Daily", "Local",
]

NOUNS = [
    "Kitchen", "Bistro", "Diner", "Dhaba", "Restaurant", "Cafe", "Grill",
    "House", "Corner", "Junction", "Treats", "Bites", "Feast", "Point",
    "Hub", "Eatery", "Foods", "Table", "Kitchen & Bar", "Spice House",
]

AREAS = [
    "MG Road", "Station Road", "Main Bazaar", "Civil Lines", "Model Town",
    "Ring Road", "Market Square", "Old City", "New Town", "Sector 5",
    "Lake View", "Central Avenue", "Park Street", "High Street", "Junction Road",
    "Mall Road", "Church Street", "Gandhi Nagar", "Nehru Place", "Green Park",
]

FLAVOR_WORDS = [
    "bold", "authentic", "homestyle", "traditional", "fusion", "comforting",
    "vibrant", "signature", "classic", "wholesome",
]


def _generate_name(used_names: set[str], city: str, rng: random.Random) -> str:
    base = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)}"
    if base not in used_names:
        used_names.add(base)
        return base
    with_city = f"{base} - {city}"
    if with_city not in used_names:
        used_names.add(with_city)
        return with_city
    i = 2
    while f"{with_city} {i}" in used_names:
        i += 1
    final = f"{with_city} {i}"
    used_names.add(final)
    return final


def _even_spread(pool: list[str], count: int, rng: random.Random) -> list[str]:
    """Returns `count` picks from `pool` with near-even usage (each image is
    used floor(count/len(pool)) or +1 times) instead of relying on pure
    randomness, which would let some images repeat far more than others by
    chance while others barely appear."""
    picks: list[str] = []
    while len(picks) < count:
        lap = pool.copy()
        rng.shuffle(lap)
        picks.extend(lap)
    return picks[:count]


def build_generated_restaurants(count: int, seed: int = 42) -> list[models.Restaurant]:
    rng = random.Random(seed)
    cities = list(CITY_COORDINATES.items())
    used_names: set[str] = set()
    hero_picks = _even_spread(HERO_IMAGES, count, rng)
    restaurants = []

    for i in range(count):
        city, (lat, lng) = rng.choice(cities)
        profile = rng.choice(CUISINE_PROFILES)
        name = _generate_name(used_names, city, rng)

        chosen_dishes = rng.sample(
            profile["dishes"], k=rng.randint(min(5, len(profile["dishes"])), len(profile["dishes"]))
        )
        price_factor = rng.uniform(0.85, 1.3)
        avg_price = sum(d[2] for d in chosen_dishes) / len(chosen_dishes) * price_factor

        restaurant = models.Restaurant(
            name=name,
            description=(
                f"A {rng.choice(FLAVOR_WORDS)} {profile['label'].split(',')[0].lower()} spot "
                f"loved by regulars in {city}."
            ),
            cuisine_type=profile["label"],
            city=city,
            address=f"{rng.choice(AREAS)}, {city}",
            latitude=lat + rng.uniform(-0.03, 0.03),
            longitude=lng + rng.uniform(-0.03, 0.03),
            rating=round(rng.uniform(3.4, 4.9), 1),
            cost_for_two=int(round(avg_price * 2, -1)),
            image_url=CDN_HERO.format(hero_picks[i]),
            is_open=rng.random() > 0.08,
        )

        categories_by_name = {}
        for idx, cat_name in enumerate(profile["categories"]):
            category = models.Category(name=cat_name, sort_order=idx)
            restaurant.categories.append(category)
            categories_by_name[cat_name] = category

        for dish_name, desc, base_price, is_veg, cat_name, tags, photo_id in chosen_dishes:
            item = models.MenuItem(
                name=dish_name,
                description=desc,
                price=round(base_price * price_factor, -1) or base_price,
                is_veg=is_veg,
                rating=round(rng.uniform(3.5, 4.9), 1),
                image_url=_img(photo_id),
                tags=tags,
                category=categories_by_name[cat_name],
            )
            restaurant.menu_items.append(item)

        restaurants.append(restaurant)

    return restaurants
