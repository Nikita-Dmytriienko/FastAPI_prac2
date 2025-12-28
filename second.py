from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def users(name, age):
    return {"user_name": name, "user_age": age}