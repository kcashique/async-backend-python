from fastapi import FastAPI
from modules.authentication import auth

application=FastAPI()
application.include_router(auth.router)