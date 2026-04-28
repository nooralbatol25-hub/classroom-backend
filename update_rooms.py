import firebase_admin
from firebase_admin import credentials, firestore
import random

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

statuses = ['reserved', 'occupied', 'free', 'free', 'free', 'noshow']

for i in range(1, 101):
    room_id = f'R{100 + i}'
    status = random.choice(statuses)
    capacity = random.choice([30, 40, 50, 60])
    db.collection("rooms").document(room_id).set({
        'room_id': room_id,
        'Capacity': capacity,
        'status': status,
    })
    print(f'✅ {room_id} - {status}')

print('🎉 100 rooms updated!')
import random

# تحديث حالة غرف التدريسيين
for i in range(1, 31):
    room_id = f'TR{i:02d}'
    status = random.choice(['free', 'free', 'reserved', 'occupied', 'noshow'])
    db.collection("rooms").document(room_id).update({'status': status})
    print(f'✅ {room_id} - {status}')

# تحديث حالة غرف الموظفين
for i in range(1, 21):
    room_id = f'ST{i:02d}'
    status = random.choice(['free', 'free', 'reserved', 'occupied', 'noshow'])
    db.collection("rooms").document(room_id).update({'status': status})
    print(f'✅ {room_id} - {status}')