\
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Tuple
from sqlalchemy import create_engine, text
import os, re

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipes")
engine = create_engine(DATABASE_URL, future=True)

app = FastAPI(title="Recipes API", version="1.0.0")

class Recipe(BaseModel):
    id: int
    title: str
    cuisine: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Optional[dict] = None
    serves: Optional[str] = None

_op_re = re.compile(r"^(<=|>=|=|<|>)\s*(\d+(?:\.\d+)?)$")

def parse_op_value(s: Optional[str]) -> Optional[Tuple[str, float]]:
    if not s:
        return None
    s = s.strip()
    m = _op_re.match(s)
    if not m:
        return None
    return m.group(1), float(m.group(2))

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/recipes")
def get_recipes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    offset = (page - 1) * limit
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM recipes")).scalar()
        rows = conn.execute(text(
            """
            SELECT id, title, cuisine, rating, prep_time, cook_time, total_time,
                   description, nutrients, serves
            FROM recipes
            ORDER BY rating DESC NULLS LAST, id ASC
            LIMIT :limit OFFSET :offset
            """
        ), {"limit": limit, "offset": offset}).mappings().all()
    return JSONResponse({"page": page, "limit": limit, "total": total, "data": [dict(r) for r in rows]})

@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating: Optional[str] = Query(None, description="Comparison like >=4.5"),
    total_time: Optional[str] = Query(None, description="Comparison like <=60"),
    calories: Optional[str] = Query(None, description="Comparison like <=400 (kcal)"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    where = []
    params = {}

    if title:
        where.append("lower(title) LIKE :title")
        params["title"] = f"%{title.lower()}%"

    if cuisine:
        where.append("lower(cuisine) = :cuisine")
        params["cuisine"] = cuisine.lower()

    rop = parse_op_value(rating)
    if rop:
        op, val = rop
        where.append(f"rating {op} :rating")
        params["rating"] = val

    top = parse_op_value(total_time)
    if top:
        op, val = top
        where.append(f"total_time {op} :total_time")
        params["total_time"] = int(val)

    cop = parse_op_value(calories)
    if cop:
        op, val = cop
        where.append("(regexp_replace(nutrients->>'calories', '[^0-9]', '', 'g'))::int " + op + " :calories")
        params["calories"] = int(val)

    clause = (" WHERE " + " AND ".join(where)) if where else ""
    offset = (page - 1) * limit

    with engine.begin() as conn:
        total = conn.execute(text(f"SELECT COUNT(*) FROM recipes{clause}"), params).scalar()
        rows = conn.execute(text(
            f"""
            SELECT id, title, cuisine, rating, prep_time, cook_time, total_time,
                   description, nutrients, serves
            FROM recipes
            {clause}
            ORDER BY rating DESC NULLS LAST, id ASC
            LIMIT :limit OFFSET :offset
            """
        ), {**params, "limit": limit, "offset": offset}).mappings().all()

    return JSONResponse({"page": page, "limit": limit, "total": total, "data": [dict(r) for r in rows]})
