from fastapi import FastAPI
from modules.authentication import auth

application=FastAPI(debug=True)
application.include_router(auth.router)

# @application.middleware('http')
# async def inject_db_obj(request: Request, call_next):
#     db_conn=ConnectionHandler()
#     await db_conn.initialize_pool()
#     request.scope['db_conn']=db_conn    
#     response= await call_next(request)
#     return response