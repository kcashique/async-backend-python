from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from modules.db_activity import ConnectionHandler
from modules.dependencies import fetch_db_conn, fetch_mongo_conn
from motor.motor_asyncio import AsyncIOMotorClient

import asyncio
import logging, uuid

router = APIRouter(prefix='/user',tags=['user'])

class UserAuth(BaseModel):
    username: str
    password: str

@router.post(path='/auth',tags=['user'])
async def authenticate_user(auth_info: UserAuth, mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
    resp={'status':'failed','message':'Error occurred'}    
    try:
        db=mgc['krib_api']            
        user_info= await db.users.find_one({'username':auth_info.username,'password':auth_info.password})
        if user_info is not None:
            access_token=uuid.uuid1().__str__()
            if await db.user_log.find_one({'username':auth_info.username}) is None:
                await db.user_log.insert_one({'username':auth_info.username,'access_token':access_token})
            else:
                await db.user_log.update_one({'username':auth_info.username},{'$set':{'access_token':access_token}})
            resp['status']='success'
            resp['message']='Authentication success'
            resp['access_token']=access_token
        else:
            resp['message']='Invalid credentials'
    except Exception as err:
        logging.error('API_ERROR(AUTH_AU) : '+str(err))
    finally:
        mgc.close()
        return resp

@router.post(path='/register',tags=['user'])
async def register_user(auth_info: UserAuth, db_conn: ConnectionHandler = Depends(fetch_db_conn), mgc: AsyncIOMotorClient = Depends(fetch_mongo_conn)):
    resp={'status':'failed','message':'Error occurred'}
    try:
        task1=asyncio.create_task(db_conn.execute_write('insert into user_master(username,password,email)values($1,$2,$3) returning user_id;',(auth_info.username,auth_info.password,'cmubeenali@gmail.com')))
        task2=asyncio.create_task(insert_user_record_mongo(auth_info=auth_info,mgc=mgc))
        await asyncio.gather(task1,task2)
        resp['status']='success'
        resp['message']='User has been registered successfully!'
    except Exception as err:
        logging.error('API_ERROR(AUTH_AU) : '+str(err))
    finally:
        return resp

async def insert_user_record_mongo(auth_info: UserAuth, mgc: AsyncIOMotorClient):
    db=mgc['krib_api']
    await db.users.insert_one({'username':auth_info.username,'password':auth_info.password})
    mgc.close()