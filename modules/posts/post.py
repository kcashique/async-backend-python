from fastapi import APIRouter, Depends
from pydantic import BaseModel

from modules.db_activity import ConnectionHandler
from modules.dependencies import fetch_db_conn, fetch_mongo_conn
from motor.motor_asyncio import AsyncIOMotorClient

import asyncio
import logging

router = APIRouter(prefix='/post',tags=['posts'])

class Post(BaseModel):
    title: str
    description: str


@router.post(path='/create_post',tags=['posts'])
async def create_post(post_info: Post, db_conn: ConnectionHandler = Depends(fetch_db_conn), mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
    resp={'db_status':'not created ','status':'failed','message':'Error occurred'}
    try:
        task1=asyncio.create_task(db_conn.execute_write("""CREATE TABLE IF NOT EXISTS post (
            post_id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            description TEXT
        );""", ()))
        resp['db_status']='created'
        task2=asyncio.create_task(db_conn.execute_write('insert into post(title,description)values($1,$2) returning post_id;',(post_info.title,post_info.description)))
        task3=asyncio.create_task(insert_post_record_mongo(post_info=post_info,mgc=mgc))

        await asyncio.gather(task2,task3)
        resp['status']='success'
        resp['message']='Post created successfully!'

    except Exception as err:
        logging.error('API_ERROR(POST_ER) : '+str(err))
    finally:
        return resp

async def insert_post_record_mongo(post_info: Post, mgc: AsyncIOMotorClient):
    db=mgc['krib_api']
    await db.users.insert_one({'title':post_info.title,'description':post_info.description})
    mgc.close()