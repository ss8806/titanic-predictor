from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# CORS設定の追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('titanic_model.pkl')

# 入力データの形式


class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    Fare: float


@app.post("/predict")
def predict_survival(passenger: Passenger):
    data = pd.DataFrame([{
        "Pclass": passenger.Pclass,
        "Sex": 1 if passenger.Sex == "male" else 0,
        "Age": passenger.Age,
        "Fare": passenger.Fare
    }])
    prediction = model.predict(data)[0]
    return {"Survived": bool(prediction)}
