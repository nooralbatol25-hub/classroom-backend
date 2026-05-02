import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("attendance").stream()
records = [doc.to_dict() for doc in docs]

with open("attendance.json", "w") as f:
    json.dump(records, f)

print(f"Saved {len(records)} records")