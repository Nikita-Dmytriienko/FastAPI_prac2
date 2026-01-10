from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    now = datetime.now()
    response = JSONResponse(content={"message": "cookies enabled"})
    response.set_cookie(key="last_visit", value=now)
    return response