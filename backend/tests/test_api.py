from app import models
from app.crud import pwd_context


def _signup(client, email="user@test.dev", password="secret123", name="Test User"):
    r = client.post("/users/signup", json={"name": name, "email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()["access_token"]


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _seed_restaurant(db_session):
    restaurant = models.Restaurant(
        name="Test Diner",
        cuisine_type="Test Cuisine",
        city="Testville",
        rating=4.5,
        cost_for_two=300,
        latitude=1.0,
        longitude=1.0,
    )
    db_session.add(restaurant)
    db_session.flush()
    category = models.Category(restaurant_id=restaurant.id, name="Mains", sort_order=0)
    db_session.add(category)
    db_session.flush()
    item = models.MenuItem(
        restaurant_id=restaurant.id,
        category_id=category.id,
        name="Test Dish",
        price=100.0,
    )
    db_session.add(item)
    db_session.commit()
    return {"restaurant_id": restaurant.id, "menu_item_id": item.id}


# ---------- Auth ----------
def test_signup_returns_token_and_user(client):
    r = client.post(
        "/users/signup",
        json={"name": "Alice", "email": "alice@test.dev", "password": "secret123"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["user"]["email"] == "alice@test.dev"
    assert data["user"]["is_staff"] is False
    assert data["access_token"]


def test_signup_duplicate_email_rejected(client):
    _signup(client, email="dup@test.dev")
    r = client.post(
        "/users/signup", json={"name": "Dup2", "email": "dup@test.dev", "password": "x"}
    )
    assert r.status_code == 400


def test_login_success(client):
    _signup(client, email="bob@test.dev", password="secret123")
    r = client.post("/users/login", json={"email": "bob@test.dev", "password": "secret123"})
    assert r.status_code == 200
    assert r.json()["access_token"]


def test_login_wrong_password_rejected(client):
    _signup(client, email="carl@test.dev", password="secret123")
    r = client.post("/users/login", json={"email": "carl@test.dev", "password": "wrong"})
    assert r.status_code == 401


def test_me_requires_token(client):
    assert client.get("/users/me").status_code == 401


def test_me_returns_current_user(client):
    token = _signup(client, email="dana@test.dev", name="Dana")
    r = client.get("/users/me", headers=_auth(token))
    assert r.status_code == 200
    assert r.json()["name"] == "Dana"


# ---------- Restaurants ----------
def test_list_restaurants(client, db_session):
    seed = _seed_restaurant(db_session)
    r = client.get("/restaurants")
    assert r.status_code == 200
    assert any(x["id"] == seed["restaurant_id"] for x in r.json())


def test_restaurant_count(client, db_session):
    _seed_restaurant(db_session)
    r = client.get("/restaurants/count")
    assert r.status_code == 200
    assert r.json()["total"] == 1


def test_get_restaurant_not_found(client):
    assert client.get("/restaurants/999").status_code == 404


# ---------- Orders ----------
def test_create_order_requires_auth(client, db_session):
    seed = _seed_restaurant(db_session)
    r = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 1}]},
    )
    assert r.status_code == 401


def test_create_order_success(client, db_session):
    seed = _seed_restaurant(db_session)
    token = _signup(client)
    r = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 2}]},
        headers=_auth(token),
    )
    assert r.status_code == 201
    data = r.json()
    assert data["total_amount"] == 200.0
    assert data["status"] == "placed"
    assert data["restaurant_name"] == "Test Diner"
    assert data["items"][0]["menu_item_name"] == "Test Dish"


def test_create_order_invalid_menu_item(client, db_session):
    seed = _seed_restaurant(db_session)
    token = _signup(client)
    r = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": 99999, "quantity": 1}]},
        headers=_auth(token),
    )
    assert r.status_code == 404


def test_create_order_empty_items_rejected(client, db_session):
    seed = _seed_restaurant(db_session)
    token = _signup(client)
    r = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": []},
        headers=_auth(token),
    )
    assert r.status_code == 404


def test_order_ownership_isolation(client, db_session):
    seed = _seed_restaurant(db_session)
    token1 = _signup(client, email="u1@test.dev")
    token2 = _signup(client, email="u2@test.dev")
    order_id = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 1}]},
        headers=_auth(token1),
    ).json()["id"]

    own = client.get(f"/orders/{order_id}", headers=_auth(token1))
    other = client.get(f"/orders/{order_id}", headers=_auth(token2))
    assert own.status_code == 200
    assert other.status_code == 403


def test_advance_status_requires_staff(client, db_session):
    seed = _seed_restaurant(db_session)
    token = _signup(client)
    order_id = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 1}]},
        headers=_auth(token),
    ).json()["id"]

    r = client.post(f"/orders/{order_id}/advance", headers=_auth(token))
    assert r.status_code == 403


def test_staff_can_advance_order_through_pipeline(client, db_session):
    seed = _seed_restaurant(db_session)
    customer_token = _signup(client, email="cust@test.dev")
    order_id = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 1}]},
        headers=_auth(customer_token),
    ).json()["id"]

    staff = models.User(
        name="Staff", email="staff@test.dev", hashed_password=pwd_context.hash("x"), is_staff=True
    )
    db_session.add(staff)
    db_session.commit()
    staff_token = client.post(
        "/users/login", json={"email": "staff@test.dev", "password": "x"}
    ).json()["access_token"]

    r1 = client.post(f"/orders/{order_id}/advance", headers=_auth(staff_token))
    assert r1.status_code == 200
    assert r1.json()["status"] == "confirmed"

    r2 = client.post(f"/orders/{order_id}/advance", headers=_auth(staff_token))
    assert r2.json()["status"] == "preparing"


def test_kitchen_view_requires_staff(client, db_session):
    _seed_restaurant(db_session)
    token = _signup(client)
    assert client.get("/orders/kitchen", headers=_auth(token)).status_code == 403


def test_invalid_status_rejected(client, db_session):
    seed = _seed_restaurant(db_session)
    customer_token = _signup(client)
    order_id = client.post(
        "/orders",
        json={"restaurant_id": seed["restaurant_id"], "items": [{"menu_item_id": seed["menu_item_id"], "quantity": 1}]},
        headers=_auth(customer_token),
    ).json()["id"]

    staff = models.User(
        name="Staff2", email="staff2@test.dev", hashed_password=pwd_context.hash("x"), is_staff=True
    )
    db_session.add(staff)
    db_session.commit()
    staff_token = client.post(
        "/users/login", json={"email": "staff2@test.dev", "password": "x"}
    ).json()["access_token"]

    r = client.patch(
        f"/orders/{order_id}/status", json={"status": "not_a_real_status"}, headers=_auth(staff_token)
    )
    assert r.status_code == 422


# ---------- Recommendations ----------
def test_popular_recommendations_returns_list(client, db_session):
    seed = _seed_restaurant(db_session)
    r = client.get(f"/recommendations/popular/{seed['restaurant_id']}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
