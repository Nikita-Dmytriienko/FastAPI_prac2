from fastapi import FastAPI, Query, status
from pydantic import BaseModel


class ExerciseRequest(BaseModel):
    weight: float
    squats: int


app = FastAPI()





@app.get("/calculate", status_code=status.HTTP_200_OK)
def calculate(weight: float = Query(ge=30, lt=150),
              squats: int = Query(ge=1, lt=500)):
    calories = squats * ( weight / 70 ) * 0.4
    calories = round(calories, 1)

    return {"Your weight": weight,
            "Amount of squats": squats,
            "Your burned calories:": calories}
