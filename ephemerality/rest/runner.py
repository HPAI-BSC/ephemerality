from fastapi import FastAPI
from ephemerality.rest import router


app = FastAPI()
app.include_router(router)
