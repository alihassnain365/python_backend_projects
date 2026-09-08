import jwt
import os
from dotenv import load_dotenv


payload = {"id": 6, "name": "eleven"}
load_dotenv()
key = os.getenv("jwt_secret_key")
algorithm = 'HS256'
print(key)

token = jwt.encode(payload, key, algorithm)
print(token)
print(type(token))

decoded = jwt.decode(token, key, algorithms=[algorithm])
print(decoded)

wrong_key = 'wrongkey123'
try:
    jwt.decode(token, wrong_key, algorithms=[algorithm])
except Exception as e:
    print("Failed as expected:", e)