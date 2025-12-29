from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def notfound():
    return {"message": "Resource Not Found"}