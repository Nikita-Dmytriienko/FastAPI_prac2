from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/")
def root(last_visit: str | None = Cookie(default=None)):
    if last_visit is None:
        return {"message": "Its your first visit"}
    else:
        return {"last visit": last_visit}