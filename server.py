from fastapi import FastAPI
from modules.authentication import auth
from modules.posts import post

# we can add each tags description here
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "posts",
        "description": "Manage posts. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "post external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

# here i add tags_metadata to open_api tags and also added project detials
app=FastAPI(debug=True, openapi_tags=tags_metadata,
    title="Krib App",
    description="Krib is a property management palatform",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },)
app.include_router(auth.router)
app.include_router(post.router)

# @application.middleware('http')
# async def inject_db_obj(request: Request, call_next):
#     db_conn=ConnectionHandler()
#     await db_conn.initialize_pool()
#     request.scope['db_conn']=db_conn    
#     response= await call_next(request)
#     return response