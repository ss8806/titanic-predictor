# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# モデルの読み込み
model = joblib.load('titanic_model.pkl')


# FastAPIのインスタンス
app = FastAPI()


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MySQLデータベースの設定
DATABASE_URL = "mysql+mysqlconnector://root:hogihogi@localhost/titanic_predictions"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# データベースのテーブルモデル
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    pclass = Column(Integer)
    sex = Column(String(10))
    age = Column(Float)
    fare = Column(Float)
    survived = Column(Boolean)
    timestamp = Column(TIMESTAMP)


# テーブルの作成
Base.metadata.create_all(bind=engine)


# 入力データの形式
class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    Fare: float


@app.post("/predict")
def predict_survival(passenger: Passenger):
    # データフレームに変換
    data = pd.DataFrame([{
        "Pclass": passenger.Pclass,
        "Sex": 1 if passenger.Sex == "male" else 0,
        "Age": passenger.Age,
        "Fare": passenger.Fare
    }])

    # 予測を実行
    prediction = model.predict(data)[0]
    survived = bool(prediction)

    # データベースに結果を保存
    db = SessionLocal()
    db_prediction = Prediction(
        pclass=passenger.Pclass,
        sex=passenger.Sex,
        age=passenger.Age,
        fare=passenger.Fare,
        survived=survived
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    db.close()

    return {"Survived": survived}
