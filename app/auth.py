from fastapi import HTTPException, Header

STATIC_TOKEN = "mysecrettoken"

def authenticate(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
