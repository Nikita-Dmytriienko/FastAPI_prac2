from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    data = "NEKETS"
    return Response(content=data)
