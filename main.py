import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize Firebase
import os
import json

cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if cred_json:
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
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

model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
model.fit(X, y)
attendance_cache = {}
# تدريب النموذج من Firebase
try:
    print("Using default training data...")
    df = pd.DataFrame(training_data)
    X_train = df[["day", "time"]]
    y_train = df["label"]
    model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    attendance_cache = {}
    print("✅ Model ready!")
except Exception as e:
    print(f"⚠️ Error: {e}")
    df = pd.DataFrame(training_data)
    X = df[["day", "time", "capacity", "prev_noshow"]]
    y = df["label"]
    model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    model.fit(X, y)
    print(f"⚠️ Error: {e}")

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
    # التحقق من جدول الجامعة
    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_name = day_names[day] if day < len(day_names) else 'Sunday'
    
    schedule_check = db.collection("schedules")\
        .where("room", "==", room_id)\
        .where("day", "==", day_name)\
        .stream()
    
    schedule_records = [doc.to_dict() for doc in schedule_check]
    
    if not schedule_records:
        return {
            "room_id": room_id,
            "noshow_probability": 0.0,
            "decision": "Keep Reservation",
            "capacity": capacity,
            "status": "available"
        }
    
    # الراندوم فورست يتنبأ فقط على القاعات المحجوزة
    

    
    # جلب احتمالية No-show من بيانات الحضور
    key = f"{room_id}-{day}"
    records = [{'noshow': n} for n in attendance_cache.get(key, [])]
    if records:
        hist_noshow = sum(r['noshow'] for r in records) / len(records)
    else:
        hist_noshow = 0.3

    features = np.array([[day, time, hist_noshow]])
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
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize Firebase
import os
import json

cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if cred_json:
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("serviceaccount.json")

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
    
    # الراندوم فورست يتنبأ فقط على القاعات المحجوزة
    # التحقق من جدول الجامعة - هل القاعة محجوزة في هذا اليوم؟
    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_name = day_names[day] if day < len(day_names) else 'Sunday'
    
    schedule_check = db.collection("schedules")\
        .where("room", "==", room_id)\
        .where("day", "==", day_name)\
        .stream()
    
    schedule_records = [doc.to_dict() for doc in schedule_check]
    
    if not schedule_records:
        return {
            "room_id": room_id,
            "noshow_probability": 0.0,
            "decision": "Keep Reservation",
            "capacity": capacity,
            "status": "available"
        }

    actual_noshow = 1 if room.get('status') == 'noshow' else 0
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
from pydantic import BaseModel

class Booking(BaseModel):
    room_id: str
    date: str
    from_time: str = ""
    to_time: str = ""
    booked_by: str = ""
    status: str = "reserved"
@app.post("/bookings")
def add_booking(booking: Booking):
    data = {
        "room_id": booking.room_id,
        "date": booking.date,
        "from": booking.from_time,
        "to": booking.to_time,
        "booked_by": booking.booked_by,
        "status": booking.status,
    }
    db.collection("bookings").add(data)
    return {"message": "Booking added successfully!"}
@app.get("/bookings/{date}")
def get_bookings(date: str):
    bookings = db.collection("bookings").where("date", "==", date).stream()
    result = []
    for b in bookings:
        result.append(b.to_dict())
    return result
@app.get("/schedules")
def get_schedules(department: str = "", stage: str = ""):
    query = db.collection("schedules")
    if department:
        query = query.where("department", "==", department)
    if stage:
        query = query.where("stage", "==", stage)
    result = []
    for doc in query.stream():
        result.append(doc.to_dict())
    return result
@app.get("/predict-staff/{room_id}")
def predict_staff_noshow(room_id: str, day: int = 0, time: int = 10):
    room_ref = db.collection("rooms").document(room_id).get()
    if not room_ref.exists:
        return {"error": "Room not found"}
    
    room = room_ref.to_dict()
    status = room.get('status', 'free')
    
    actual_noshow = 1 if status in ['noshow', 'reserved'] else 0
    capacity = room.get('Capacity', 1)
    
    features = np.array([[day, time, capacity, actual_noshow]])
    prob = model.predict_proba(features)[0][1]
    prediction = "Candidate (Reallocate)" if prob > 0.65 else "Monitor" if prob > 0.45 else "Keep Reservation"
    
    return {
        "room_id": room_id,
        "noshow_probability": round(prob, 2),
        "decision": prediction,
        "status": status
    }
@app.get("/schedule-by-day")
def get_schedule_by_day(day: str):
    schedules = db.collection("schedules").where("day", "==", day).stream()
    result = []
    for s in schedules:
        result.append(s.to_dict())
    return result
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8000,) 
  
 
  