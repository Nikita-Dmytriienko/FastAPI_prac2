from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse

app = FastAPI()

@app.get("/html", response_class= HTMLResponse)
def root_html():
    data = "<h1> NEKETS <h1>"
    return HTMLResponse(content=data)

@app.get("/text", response_class=PlainTextResponse)
def root_text():
    data = "<NEKETS>"
    return PlainTextResponse(content=data)