from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import menu, orders, recommendations, restaurants, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Hotel — Menu API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(recommendations.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "mini-hotel-api"}
