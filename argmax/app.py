import uvicorn
from fastapi import FastAPI
from .api import users


app = FastAPI()
app.include_router(users.router)


def start():
    uvicorn.run("argmax.app:app", host="localhost", port=8080, reload=True)