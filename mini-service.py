'''
Раз разобрался с Query Params,
 попробуй реализовать мини-сервис,
  который принимает параметры (например,
   твой вес и количество прыжков) и возвращает расчет сожженных калорий с правильным статусным кодом.
'''

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/weight")
def weight(weight: float = Query(ge=30, lt=150):
    
