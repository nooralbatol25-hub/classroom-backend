import firebase_admin
from firebase_admin import credentials, firestore
import random
import json

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# قراءة جداول الجامعة
with open("ism_schedules.json", "r") as f:
    ism_data = json.load(f)

with open("bit_schedules.json", "r", encoding="utf-8") as f:
    bit_data = json.load(f)

# تصحيح أسماء قاعات BIT
def fix_room_name(room):
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
    return room

day_to_num = {
    'Sunday': 0, 'Monday': 1, 'Tuesday': 2,
    'Wednesday': 3, 'Thursday': 4
}

attendance_records = []

# توليد بيانات من ISM
for stage in ism_data["stages"]:
    for day_schedule in stage["schedule"]:
        day = day_schedule["day"]
        for session in day_schedule["sessions"]:
            # توليد 10 سجلات تاريخية لكل حصة
            for week in range(10):
                # احتمالية الحضور حسب الوقت واليوم
                time_start = int(session["time"].split(":")[0])
                noshow_prob = 0.4  # افتراضي
                
                if time_start <= 9:  # صباح باكر
                    noshow_prob = 0.7
                if day in ['Sunday', 'Thursday']:  # بداية ونهاية الأسبوع
                    noshow_prob += 0.1
                    
                noshow = 1 if random.random() < noshow_prob else 0
                
                attendance_records.append({
                    "department": "ISM",
                    "stage": stage["stage_name"],
                    "day": day,
                    "day_num": day_to_num.get(day, 0),
                    "time": session["time"],
                    "time_num": time_start,
                    "room": session["room"],
                    "subject": session["subject"],
                    "week": week + 1,
                    "noshow": noshow
                })

# توليد بيانات من BIT
for stage in bit_data["stages"]:
    for day_schedule in stage["schedule"]:
        day = day_schedule["day"]
        for session in day_schedule["sessions"]:
            for week in range(10):
                time_start = int(session["time"].split(":")[0])
                noshow_prob = 0.2
                
                if time_start <= 9:
                    noshow_prob = 0.4
                if day in ['Sunday', 'Thursday']:
                    noshow_prob += 0.1
                    
                noshow = 1 if random.random() < noshow_prob else 0
                
                room = fix_room_name(session["room"])
                
                attendance_records.append({
                    "department": "BIT",
                    "stage": stage["stage_name"],
                    "day": day,
                    "day_num": day_to_num.get(day, 0),
                    "time": session["time"],
                    "time_num": time_start,
                    "room": room,
                    "subject": session["subject"],
                    "week": week + 1,
                    "noshow": noshow
                })

# رفع للـ Firebase
print(f"📊 Total records: {len(attendance_records)}")
for i, record in enumerate(attendance_records):
    db.collection("attendance").add(record)
    if i % 50 == 0:
        print(f"✅ Uploaded {i}/{len(attendance_records)}")

print("🎉 Done!")