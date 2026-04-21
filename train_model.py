import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

np.random.seed(42)
n = 50

data = {
    "day": np.random.randint(0, 5, n),
    "time": np.random.randint(8, 17, n),
    "capacity": np.random.choice([30, 40, 50, 60], n),
    "prev_noshow": np.random.randint(0, 2, n),
}

df = pd.DataFrame(data)
df["label"] = np.where(df["prev_noshow"] == 1,
    np.random.choice([0,1], n, p=[0.3, 0.7]),
    np.random.choice([0,1], n, p=[0.8, 0.2]))

X = df[["day", "time", "capacity", "prev_noshow"]]
y = df["label"]

import pickle
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Random Forest Model saved!")