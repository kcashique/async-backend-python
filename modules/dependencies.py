from fastapi import Request

def fetch_db_conn(request: Request):
    db_conn=request.scope['db_conn']
    return db_conn