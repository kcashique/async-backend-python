from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from datetime import datetime

import asyncio
from random import randint

async def coro1():
    print('executing query : '+str(randint(0,1000)))
    await asyncio.sleep(randint(0,5))

async def auth_login(request):
    cur_loop= asyncio.get_running_loop()
    cur_loop.create_task(coro1())
    return JSONResponse({'status':'success','logged_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')})

application=Starlette(debug=True, routes=[
    Route('/login',auth_login)
])