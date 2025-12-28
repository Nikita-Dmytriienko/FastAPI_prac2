from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def users_phone_number(phone: str = Query(pattern=r"^\d{10}$")):
    return {"user_phone_number": phone}