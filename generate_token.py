from jose import jwt
import datetime

# المفتاح السري الثابت
JWT_SECRET_KEY = "078256"
ALGORITHM = "HS256"

def create_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

# توليد التوكن
print("توكن تسجيل الدخول الخاص بك هو:")
print(create_token("mazin"))
