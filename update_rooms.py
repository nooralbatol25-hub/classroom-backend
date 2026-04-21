import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

rooms_data = [
    {"room_id": "R101", "Capacity": 35, "status": "reserved"},
    {"room_id": "R102", "Capacity": 40, "status": "occupied"},
    {"room_id": "R103", "Capacity": 30, "status": "free"},
    {"room_id": "R104", "Capacity": 50, "status": "reserved"},
    {"room_id": "R105", "Capacity": 30, "status": "reserved"},
    {"room_id": "R106", "Capacity": 40, "status": "free"},
    {"room_id": "R107", "Capacity": 35, "status": "reserved"},
    {"room_id": "R108", "Capacity": 30, "status": "free"},
    {"room_id": "R109", "Capacity": 40, "status": "noshow"},
    {"room_id": "R110", "Capacity": 60, "status": "occupied"},
    {"room_id": "R111", "Capacity": 40, "status": "occupied"},
    {"room_id": "R112", "Capacity": 40, "status": "reserved"},
    {"room_id": "R113", "Capacity": 30, "status": "free"},
    {"room_id": "R114", "Capacity": 35, "status": "free"},
    {"room_id": "R115", "Capacity": 30, "status": "free"},
    {"room_id": "R116", "Capacity": 40, "status": "free"},
    {"room_id": "R117", "Capacity": 35, "status": "free"},
    {"room_id": "R118", "Capacity": 25, "status": "reserved"},
    {"room_id": "R119", "Capacity": 30, "status": "occupied"},
    {"room_id": "R120", "Capacity": 40, "status": "free"},
]

for room in rooms_data:
    db.collection("rooms").document(room["room_id"]).set(room)
    print(f"Updated {room['room_id']} - {room['status']}")

print("All rooms updated!")