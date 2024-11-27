import json

import redis

from Intuit.MyBook.src.config.config import REDIS_CONFIG
from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.models.user import User
from fastapi import HTTPException
import bcrypt
from redis import asyncio as aioredis

# Redis client for caching
#redis = aioredis.from_url("redis://localhost")

r = redis.Redis(**REDIS_CONFIG)
async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



async def create_user(user: User):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        hashed_password = await hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (email, password, first_name, last_name, locale, currency) VALUES (%s, %s, %s, "
            "%s, %s,"
            "%s) RETURNING id",
            (user.email, hashed_password, user.first_name, user.last_name, user.locale, user.currency)
        )
        user_id = cursor.fetchone()['id']
        conn.commit()
        return {"id": user_id, **user.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

async def get_user(user_id: int):
    t = r.get(user_id)
    if t:
        t = json.loads(t)
        if t:
            return t
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            r.set(user_id, json.dumps(user))
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        cursor.close()
        conn.close()