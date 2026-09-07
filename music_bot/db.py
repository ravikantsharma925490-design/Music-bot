"""
MongoDB database module (Motor - async driver).

Ye module 2 cheezein persistently store karta hai:
1. Activated groups (jo /start se activate ho chuke hain)
2. Har group ki language setting (hindi/english)

App start hone par saara data MongoDB se load karke memory me cache
kar liya jata hai (fast access ke liye), aur har change turant DB me
bhi save ho jata hai.
"""

import motor.motor_asyncio

import config

_client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URI)
_db = _client[config.DB_NAME]

activated_groups_col = _db["activated_groups"]
chat_language_col = _db["chat_language"]


# ---------- Activated Groups ----------

async def add_activated_group(chat_id: int):
    await activated_groups_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )


async def get_all_activated_groups() -> set:
    cursor = activated_groups_col.find({})
    return {doc["chat_id"] async for doc in cursor}


# ---------- Chat Language ----------

async def set_chat_language(chat_id: int, lang_code: str):
    await chat_language_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang_code}},
        upsert=True,
    )


async def get_all_chat_languages() -> dict:
    cursor = chat_language_col.find({})
    return {doc["chat_id"]: doc["lang"] async for doc in cursor}


async def ping():
    """Startup par MongoDB connection test karne ke liye"""
    await _client.admin.command("ping")
