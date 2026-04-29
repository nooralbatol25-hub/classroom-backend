import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# حذف البيانات القديمة
docs = db.collection("schedules").stream()
for doc in docs:
    doc.reference.delete()
print("✅ Old schedules deleted!")

# رفع بيانات القاعات الحقيقية
rooms = [
    {"room_id": "CLASS 2", "Capacity": 40, "status": "free", "type": "classroom"},
    {"room_id": "CLASS 5", "Capacity": 40, "status": "free", "type": "classroom"},
    {"room_id": "CLASS 8", "Capacity": 40, "status": "free", "type": "classroom"},
    {"room_id": "LAB 1", "Capacity": 30, "status": "free", "type": "lab"},
    {"room_id": "LAB 2", "Capacity": 30, "status": "free", "type": "lab"},
    {"room_id": "LAB 3", "Capacity": 30, "status": "free", "type": "lab"},
    {"room_id": "LAB 4", "Capacity": 30, "status": "free", "type": "lab"},
]

for room in rooms:
    db.collection("rooms").document(room["room_id"]).set(room)
    print(f"✅ Added: {room['room_id']}")

# رفع جداول ISM
with open("ism_schedules.json", "r") as f:
    ism_data = json.load(f)

for stage in ism_data["stages"]:
    for day_schedule in stage["schedule"]:
        for session in day_schedule["sessions"]:
            doc = {
                "department": "ISM",
                "stage": stage["stage_name"],
                "day": day_schedule["day"],
                "time": session["time"],
                "subject": session["subject"],
                "room": session["room"],
                "type": session["type"],
                "status": "reserved"
            }
            db.collection("schedules").add(doc)
            print(f"✅ {stage['stage_name']} - {day_schedule['day']} - {session['room']}")
            # رفع جداول BIT
with open("bit_schedules.json", "r") as f:
    bit_data = json.load(f)
    # تصحيح أسماء القاعات في BIT
# تصحيح أسماء القاعات في BIT
for stage in bit_data["stages"]:
    for day_schedule in stage["schedule"]:
        for session in day_schedule["sessions"]:
            room = session["room"]
            room = room.replace("Classroom 1", "CLASS 1")
            room = room.replace("Classroom 6", "CLASS 6")
            room = room.replace("Classroom 7", "CLASS 7")
            room = room.replace("Class 1", "CLASS 1")
            room = room.replace("Class 6", "CLASS 6")
            room = room.replace("Class 7", "CLASS 7")
            room = room.replace("BIC_BIT_LAB1", "BIT LAB 1")
            room = room.replace("BIC_BIT_LAB2", "BIT LAB 2")
            room = room.replace("BIC_BIT_LAB3", "BIT LAB 3")
            room = room.replace("BIC_BIT_LAB4", "BIT LAB 4")
            session["room"] = room
for stage in bit_data["stages"]:
    for day_schedule in stage["schedule"]:
        for session in day_schedule["sessions"]:
            doc = {
                "department": "BIT",
                "stage": stage["stage_name"],
                "day": day_schedule["day"],
                "time": session["time"],
                "subject": session["subject"],
                "room": session["room"],
                "type": session["type"],
                "status": "reserved"
            }
            db.collection("schedules").add(doc)
            print(f"✅ BIT - {stage['stage_name']} - {day_schedule['day']} - {session['room']}")            

# غرف التدريسيين
for i in range(1, 31):
    staff_rooms.append({
        "room_id": f"TR{i:02d}",
        "Capacity": 3,
        "status": "free",
        "type": "staff_room",
        "category": "Teaching Staff"
    })

# غرف الموظفين
for i in range(1, 21):
    staff_rooms.append({
        "room_id": f"ST{i:02d}",
        "Capacity": 3,
        "status": "free",
        "type": "staff_room",
        "category": "Administrative Staff"
    })

for room in staff_rooms:
    db.collection("rooms").document(room["room_id"]).set(room)
    print(f"✅ Added: {room['room_id']} - {room['category']}")

print("🎉 Done!")