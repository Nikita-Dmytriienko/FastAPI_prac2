from fastapi import FastAPI


app = FastAPI()


@app.get("/users/admin")
def admin():
    return {"message": "Admin"}
    
@app.get("/users/{name}")
def users(name):
    return {"user_name": name}
    