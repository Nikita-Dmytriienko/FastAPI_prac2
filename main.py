from fastapi import FastAPI


app = FastAPI()


@app.get("/users/admin")
def admin():
    return {"message": "Admin"}
    
@app.get("/users/{name}")
def users(name: str):
    return {"user_name": name}

@app.get("/users/{id}")
def users(id: int):
    return {"user_id": id}
    