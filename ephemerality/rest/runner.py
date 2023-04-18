from fastapi import FastAPI
from rest import router


app = FastAPI()
app.include_router(router)
