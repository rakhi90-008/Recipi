\
import json
import math
import os
import re
from typing import Any, Dict

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/recipes")
JSON_PATH = os.environ.get("RECIPES_JSON", "../data/US_recipes.json")

def _nan_to_none(v: Any):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return None if (isinstance(v, float) and math.isnan(v)) else v
    if isinstance(v, str):
        s = v.strip().lower()
        return None if s in ("nan", "", "null", "none") else v
    return v

def _cleanup_record(obj: Dict[str, Any]) -> Dict[str, Any]:
    rec = {
        "cuisine": obj.get("cuisine"),
        "title": obj.get("title"),
        "rating": _nan_to_none(obj.get("rating")),
        "prep_time": _nan_to_none(obj.get("prep_time")),
        "cook_time": _nan_to_none(obj.get("cook_time")),
        "total_time": _nan_to_none(obj.get("total_time")),
        "description": obj.get("description"),
        "nutrients": obj.get("nutrients") or {},
        "serves": obj.get("serves"),
    }
    for k in ("prep_time", "cook_time", "total_time"):
        v = rec[k]
        if isinstance(v, str):
            m = re.search(r"-?\d+", v)
            rec[k] = int(m.group()) if m else None
    if isinstance(rec["rating"], str):
        try:
            rec["rating"] = float(rec["rating"]) if rec["rating"].lower() != "nan" else None
        except ValueError:
            rec["rating"] = None
    return rec

def _load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        for item in data:
            yield item
    elif isinstance(data, dict):
        for k in sorted(data.keys(), key=lambda x: int(x) if str(x).isdigit() else str(x)):
            yield data[k]
    else:
        raise ValueError("Unsupported JSON top-level structure")

def _ensure_schema(engine: Engine):
    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                cuisine        VARCHAR(255),
                title          VARCHAR(512) NOT NULL,
                rating         DOUBLE PRECISION,
                prep_time      INTEGER,
                cook_time      INTEGER,
                total_time     INTEGER,
                description    TEXT,
                nutrients      JSONB,
                serves         VARCHAR(128),
                created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        ))

def main():
    engine = create_engine(DATABASE_URL, future=True)
    _ensure_schema(engine)

    rows = []
    for raw in _load_json(JSON_PATH):
        rec = _cleanup_record(raw)
        if not rec.get("title"):
            continue
        rows.append(rec)

    with engine.begin() as conn:
        # Clear and load; swap to UPSERT if you need incremental
        conn.execute(text("DELETE FROM recipes"))
        for rec in rows:
            conn.execute(text(
                """
                INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time,
                                     description, nutrients, serves)
                VALUES (:cuisine, :title, :rating, :prep_time, :cook_time, :total_time,
                        :description, CAST(:nutrients AS JSONB), :serves)
                """
            ), rec)

    print(f"Loaded {len(rows)} recipes into the database.")

if __name__ == "__main__":
    main()
