from fastapi import FastAPI, Depends
from app.routes import router
from app.auth import authenticate

app = FastAPI()
app.include_router(router, dependencies=[Depends(authenticate)])