from fastapi import FastAPI, Path


app = FastAPI()


@app.get("/users/admin")
def admin():
    return {"message": "Admin"}
    
@app.get("/users/name/{name}")
def users(name: str = Path(min_length=3, max_length=16)):
    return {"user_name": name}

@app.get("/users/age/{age}")
def users(age: int = Path(ge = 18, lt = 100)):
    return {"user_age": age}
          
@app.get("/users/id/{id}")
def users(id: int):
    return {"user_id": id}

@app.get("/users/phone/{phone}")
def users(phone:str  = Path(pattern=r"^\d{11}$")):
    return {"phone": phone}
    