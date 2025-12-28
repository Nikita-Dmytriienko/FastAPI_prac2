from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def users(name: str = Query(min_length=3, max_length=20)):
    return {"name": name}