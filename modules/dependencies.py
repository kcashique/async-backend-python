from fastapi import Request
from .db_activity import ConnectionHandler
import motor.motor_asyncio

async def fetch_db_conn():
    db_conn=ConnectionHandler()
    await db_conn.initialize_pool()
    return db_conn

def fetch_mongo_conn():
    return motor.motor_asyncio.AsyncIOMotorClient('localhost',27017,connect=True)    