from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse

app = FastAPI()

@app.get("/")
def root():
    data = "<h1> NEKETS <h1>"
    return HTMLResponse(content=data)
