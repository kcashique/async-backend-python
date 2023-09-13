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
   

    async def execute_read(self, query):    # removed params in execute_read function
        data=[]
        try:
            async with self.pool.acquire() as conn:                
                result= await conn.fetch(query)
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
        

    # async def create_table(self, query):
    #     async def create_table_with_query(self, query):
    #         resp={'status':'failed','message':'Error occurred'}    
    #         try:
    #             async with self.pool.acquire() as conn:
    #                 await conn.execute(query)
    #                 resp['status']='success'
    #                 resp['message']='Table created'
    #         except Exception as err:
    #             logging.error("DB_ERROR(ER) : " + str(err))
    #         finally:
    #             return resp
            