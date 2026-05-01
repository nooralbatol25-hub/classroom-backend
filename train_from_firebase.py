import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# جلب بيانات الحضور من Firebase
print("📊 Fetching attendance data...")
docs = db.collection("attendance").stream()
records = [doc.to_dict() for doc in docs]
print(f"✅ Got {len(records)} records")

df = pd.DataFrame(records)

X = df[["day_num", "time_num", "noshow"]]
y = df["noshow"]

# تدريب النموذج
model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
model.fit(X, y)

# حفظ النموذج
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")