from fastapi import FastAPI
from dotenv import load_dotenv

from routes import router

load_dotenv()
app = FastAPI()
app.include_router(router)


@app.get("/")
def hello():
    return "Hello world"
