from fastapi import FastAPI
from modules.authentication import auth
from modules.posts import post


app=FastAPI(debug=True)
app.include_router(auth.router)
app.include_router(post.router)

# @application.middleware('http')
# async def inject_db_obj(request: Request, call_next):
#     db_conn=ConnectionHandler()
#     await db_conn.initialize_pool()
#     request.scope['db_conn']=db_conn    
#     response= await call_next(request)
#     return response