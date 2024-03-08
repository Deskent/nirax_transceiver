import uvicorn
from fastapi import FastAPI

from ws_router.connect import connect_ws

app = FastAPI()
connect_ws(app)


if __name__ == '__main__':
    uvicorn.run('main:app')
