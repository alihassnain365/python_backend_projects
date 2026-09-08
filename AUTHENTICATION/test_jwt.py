import jwt

payload = {"id": 6, "name": "eleven"}
key = 'Tribe666@'
algorithm = 'HS256'

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