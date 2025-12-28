from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def users(name: str = Query(min_length=3, max_length=20),
          age: int = Query(ge=18, lt = 100)):
    return {"user_name": name, "user_age":age}