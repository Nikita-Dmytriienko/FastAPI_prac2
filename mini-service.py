from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field


class ExerciseRequest(BaseModel):
    weight: float = Field(ge=30, lt=150, description="Weight in kg", example=70.0)
    squats: int = Field(ge=1, le=10000, description="Squats amount", example=100)


class ExerciseResponse(BaseModel):
    weight: float = Field(description="Weight in kg", example=70.0)
    squats: int = Field(description="Squats amount", example=100)
    burned_calories: float = Field(description="Burned calories", example=40.0)


app = FastAPI()


@app.get("/calculate", status_code=status.HTTP_200_OK)
def calculate_get(weight: float = Query(ge=30, lt=150),
              squats: int = Query(ge=1, lt=500)):
    calories = squats * ( weight / 70 ) * 0.4
    calories = round(calories, 1)

    return {"Your weight": weight,
            "Amount of squats": squats,
            "Your burned calories:": calories}

@app.post("/calculate", status_code=status.HTTP_200_OK, response_model=ExerciseResponse)
def calculate_post(request: ExerciseRequest) -> ExerciseResponse:
    calories = round(request.squats * (request.weight / 70) * 0.4, 1)

    return ExerciseResponse(weight = request.weight,
                            squats = request.squats,
                            burned_calories = calories)