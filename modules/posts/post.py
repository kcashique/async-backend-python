from fastapi import APIRouter, Depends, HTTPException
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
    created_by : str


# @router.post(path='/create_post',tags=['posts'])
# async def create_post(post_info: Post, db_conn: ConnectionHandler = Depends(fetch_db_conn), mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
#     resp={'db_status':'not created ','status':'failed','message':'Error occurred'}
#     try:
#         task1=asyncio.create_task(db_conn.execute_write("""CREATE TABLE IF NOT EXISTS post (
#             post_id SERIAL PRIMARY KEY,
#             title VARCHAR(255),
#             description TEXT
#         );""", ()))
#         resp['db_status']='created'
#         task2=asyncio.create_task(db_conn.execute_write('insert into post(title,description)values($1,$2) returning post_id;',(post_info.title,post_info.description)))
#         task3=asyncio.create_task(insert_post_record_mongo(post_info=post_info,mgc=mgc))

#         await asyncio.gather(task2,task3)
#         resp['status']='success'
#         resp['message']='Post created successfully!'

#     except Exception as err:
#         logging.error('API_ERROR(POST_ER) : '+str(err))
#     finally:
#         return resp

# async def insert_post_record_mongo(post_info: Post, mgc: AsyncIOMotorClient):
#     db=mgc['krib_api']
#     await db.post.insert_one({'title':post_info.title,'description':post_info.description})
#     mgc.close()


# @router.get(path='/read_posts',tags=['posts'])
# async def read_post(mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
#     resp = {'status': 'failed', 'data': 'Error occurred'}

#     try:
#         db = mgc['krib_api']
#         cursor = db.post.find({}, {"_id": 0, "title": 1, "description": 1})  # Project only title and description

#         data = []
#         async for document in cursor:
#             data.append(document)


#         if data:
#             resp["status"] = "success"
#             resp["data"] = data
#         else:
#             resp["data"] = "No data available"

#     except Exception as err:
#         logging.error('API_ERROR(AUTH_AU): ' + str(err))
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     finally:
#         mgc.close()

#     return resp

class PostCreate(BaseModel):
    title: str
    description: str
    created_by : int

@router.post(path='/create_post',tags=['posts'])
async def create_post(post_info: PostCreate, db_conn: ConnectionHandler = Depends(fetch_db_conn), mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
    resp={'status':'failed','message':'Error occurred'}
    try:
        task1=asyncio.create_task(db_conn.execute_write('insert into post(title,description, created_by)values($1,$2,$3) returning post_id;',(post_info.title,post_info.description, post_info.created_by)))
        task2=asyncio.create_task(insert_post_record_mongo(post_info=post_info,mgc=mgc))

        await asyncio.gather(task1,task2)
        resp['status']='success'
        resp['message']='Post created successfully!'

    except Exception as err:
        logging.error('API_ERROR(POST_ER) : '+str(err))
    finally:
        return resp

async def insert_post_record_mongo(post_info: Post, mgc: AsyncIOMotorClient):
    db=mgc['krib_api']
    await db.post.insert_one({'title':post_info.title,'description':post_info.description, 'created_by':post_info.created_by})
    mgc.close()


@router.get(path='/read_posts',tags=['posts'])
async def read_post(db_conn: ConnectionHandler = Depends(fetch_db_conn), mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
    resp = {'status': 'failed', 'data': 'Error occurred'}

    try:
        result = await db_conn.execute_read_listgit ('SELECT p.title, p.description, u.username as created_by FROM post p JOIN user_master u ON p.created_by = u.user_id;')

        if result:
            # Convert the result to a list of Post Pydantic models
            data = [Post(**row) for row in result]
            resp["status"] = "success"
            resp["data"] = data
        else:
            resp["data"] = "No data available"

    except Exception as err:
        logging.error('API_ERROR(AUTH_AU): ' + str(err))
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        pass
    return resp