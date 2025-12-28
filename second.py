from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def users(people: list[str] = Query()):
    return {"people": people}