import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize Firebase
cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Training data for Random Forest
training_data = [
    {"day": 0, "time": 8, "capacity": 30, "prev_noshow": 1, "label": 1},
    {"day": 0, "time": 10, "capacity": 40, "prev_noshow": 1, "label": 1},
    {"day": 1, "time": 9, "capacity": 35, "prev_noshow": 0, "label": 0},
    {"day": 2, "time": 11, "capacity": 60, "prev_noshow": 0, "label": 0},
    {"day": 3, "time": 8, "capacity": 25, "prev_noshow": 1, "label": 1},
    {"day": 4, "time": 14, "capacity": 30, "prev_noshow": 1, "label": 1},
    {"day": 0, "time": 12, "capacity": 50, "prev_noshow": 0, "label": 0},
    {"day": 1, "time": 15, "capacity": 35, "prev_noshow": 1, "label": 1},
    {"day": 2, "time": 10, "capacity": 40, "prev_noshow": 0, "label": 0},
    {"day": 3, "time": 13, "capacity": 30, "prev_noshow": 1, "label": 1},
]

df = pd.DataFrame(training_data)
X = df[["day", "time", "capacity", "prev_noshow"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

@app.get("/")
def root():
    return {"message": "Classroom Booking API is running!"}

@app.get("/rooms")
def get_rooms():
    rooms = db.collection("rooms").stream()
    result = []
    for room in rooms:
        result.append(room.to_dict())
    return result

@app.get("/predict/{room_id}")
def predict_noshow(room_id: str, day: int = 0, time: int = 10, prev_noshow: int = 0):
    room_ref = db.collection("rooms").document(room_id).get()
    if not room_ref.exists:
        return {"error": "Room not found"}
    
    room = room_ref.to_dict()
    capacity = room.get("Capacity", 30)
    
    actual_noshow = 1 if room.get('status') in ['noshow', 'reserved'] else 0
    features = np.array([[day, time, capacity, actual_noshow]])
    prob = model.predict_proba(features)[0][1]
    prediction = "Candidate (Reallocate)" if prob > 0.65 else "Monitor" if prob > 0.45 else "Keep Reservation"
    
    return {
        "room_id": room_id,
        "noshow_probability": round(prob, 2),
        "decision": prediction,
        "capacity": capacity,
        "status": room.get("status", "unknown")
    }

@app.get("/seed")
def seed_rooms():
    rooms = [
        {"room_id": f"R{100+i}", "Capacity": 30 + (i % 4) * 10, "status": "free"}
        for i in range(1, 21)
    ]
    for room in rooms:
        db.collection("rooms").document(room["room_id"]).set(room)
    return {"message": "20 rooms added to Firebase!"}
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8000,)