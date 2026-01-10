from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
def root():
    data = "Nekets"
    return Response(content=data, media_type="text/plain", headers={"Secret-Code": "12331231"})
