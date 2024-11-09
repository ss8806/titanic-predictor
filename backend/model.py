# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# データの読み込み
df = pd.read_csv("train.csv")

# 必要なカラムを選択
df['Sex'] = df['Sex'].map({'male': 1, 'female': 0})
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Fare'].fillna(df['Fare'].median(), inplace=True)

X = df[['Pclass', 'Sex', 'Age', 'Fare']]
y = df['Survived']

# データの分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# モデルの初期化とトレーニング
model = RandomForestClassifier()
model.fit(X_train, y_train)

# モデルの精度を表示
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2f}")

# 学習済みモデルの保存
joblib.dump(model, 'titanic_model.pkl')
print("Model saved as 'titanic_model.pkl'")
