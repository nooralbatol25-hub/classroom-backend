import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred)

users = [
    # Admin
    {"email": "admin@classroom.com", "password": "Admin@2026", "name": "admin"},
    
    # Teachers
    {"email": "teacher1@classroom.com", "password": "Teacher1@2026", "name": "teacher1"},
    {"email": "teacher2@classroom.com", "password": "Teacher2@2026", "name": "teacher2"},
    {"email": "teacher3@classroom.com", "password": "Teacher3@2026", "name": "teacher3"},
    {"email": "teacher4@classroom.com", "password": "Teacher4@2026", "name": "teacher4"},
    {"email": "teacher5@classroom.com", "password": "Teacher5@2026", "name": "teacher5"},
    {"email": "teacher6@classroom.com", "password": "Teacher6@2026", "name": "teacher6"},
    {"email": "teacher7@classroom.com", "password": "Teacher7@2026", "name": "teacher7"},
    {"email": "teacher8@classroom.com", "password": "Teacher8@2026", "name": "teacher8"},
    {"email": "teacher9@classroom.com", "password": "Teacher9@2026", "name": "teacher9"},
    {"email": "teacher10@classroom.com", "password": "Teacher10@2026", "name": "teacher10"},
    
    # Staff
    {"email": "staff1@classroom.com", "password": "Staff1@2026", "name": "staff1"},
    {"email": "staff2@classroom.com", "password": "Staff2@2026", "name": "staff2"},
    {"email": "staff3@classroom.com", "password": "Staff3@2026", "name": "staff3"},
    {"email": "staff4@classroom.com", "password": "Staff4@2026", "name": "staff4"},
    {"email": "staff5@classroom.com", "password": "Staff5@2026", "name": "staff5"},
    {"email": "staff6@classroom.com", "password": "Staff6@2026", "name": "staff6"},
    {"email": "staff7@classroom.com", "password": "Staff7@2026", "name": "staff7"},
    {"email": "staff8@classroom.com", "password": "Staff8@2026", "name": "staff8"},
    {"email": "staff9@classroom.com", "password": "Staff9@2026", "name": "staff9"},
]

for user in users:
    try:
        auth.create_user(
            email=user["email"],
            password=user["password"],
            display_name=user["name"]
        )
        print(f"✅ Created: {user['email']} / {user['password']}")
    except Exception as e:
        print(f"❌ Error {user['email']}: {e}")

print("🎉 Done!")