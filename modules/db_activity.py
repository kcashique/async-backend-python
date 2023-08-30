import asyncpg 
import logging

class ConnectionHandler:
    def __init__(self) -> None:
        try:
            self.pool=None
        except Exception as err:
            logging.error("DB_ERROR(INIT) : "+str(err))
    async def initialize_pool(self):
        try:
            self.pool= await asyncpg.create_pool(host='127.0.0.1',port=5432,user='krib_user',password='krib_123',database='krib_testdb',max_size=20)
        except Exception as err:
            logging.error('DB_ERROR(INIT_POOL) : '+str(err))            
   
   
    async def execute_read(self, query, params):
        data=[]
        try:
            async with self.pool.acquire() as conn:                
                result= await conn.fetch(query, params)
                for row in result:
                    data.append(row)
                await self.pool.release(conn)
        except Exception as err:
            logging.error("DB_ERROR(ER) : "+str(err))
        finally:
            return data
    async def execute_write(self, query, params):
        data=0
        try:
            async with self.pool.acquire() as conn:
                result= await conn.fetchval(query, *params)
                if result>0:
                    data=result
                await self.pool.release(conn)
        except Exception as err:
            logging.error("DB_ERROR(ER) : "+str(err))
        finally:
            return data
        
