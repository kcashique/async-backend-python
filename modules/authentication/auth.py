from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient

import logging, uuid

router=APIRouter(prefix='/user',tags=['user'])

class UserAuth(BaseModel):
    username: str
    password: str

@router.post(path='/auth',tags=['user'])
async def authenticate_user(auth_info: UserAuth):    
    resp={'status':'failed','message':'Error occurred'}
    mgc=MongoClient()
    try:        
        db=mgc['krib_api']
        user_info= db.users.find_one({'username':auth_info.username,'password':auth_info.password})
        if user_info is not None:
            access_token=uuid.uuid1().__str__()
            if db.user_log.find_one({'username':auth_info.username}) is None:
                db.user_log.insert_one({'username':auth_info.username,'access_token':access_token})
            else:
                db.user_log.update_one({'username':auth_info.username},{'$set':{'access_token':access_token}})
            resp['status']='success'
            resp['message']='Authentication success'
            resp['access_token']=access_token
        else:
            resp['message']='Invalid credentials'
        return resp
    except Exception as err:
        logging.error('API_ERROR(AUTH_AU) : '+str(err))
    finally:
        mgc.close()
        return resp