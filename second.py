from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def users(name: str | None = Query(default = None,min_length=2)):
    if name == None:
        return {"name": "Undefined"}
    else:
        return {"name": name}
    