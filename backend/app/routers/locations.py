from fastapi import APIRouter, HTTPException

from app.data.india_locations import INDIA_LOCATIONS

router = APIRouter(prefix="/locations", tags=["locations"])


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


@router.get("/states")
def list_states():
    return [
        {
            "slug": _slugify(s["name"]),
            "name": s["name"],
            "type": s["type"],
            "city_count": len(s["cities"]),
            "note": s.get("note"),
        }
        for s in INDIA_LOCATIONS
    ]


@router.get("/states/{slug}/cities")
def list_cities(slug: str):
    for s in INDIA_LOCATIONS:
        if _slugify(s["name"]) == slug:
            return {
                "slug": slug,
                "name": s["name"],
                "type": s["type"],
                "note": s.get("note"),
                "cities": s["cities"],
            }
    raise HTTPException(status_code=404, detail="State or union territory not found")
