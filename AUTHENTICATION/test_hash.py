import bcrypt

password = "hello"
hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

hash2 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

if hash1 == hash2:
    print("they are same")
else:
    print("not same")

print(bcrypt.checkpw("hello".encode('utf-8'), hash1))
print(bcrypt.checkpw("hello".encode('utf-8'), hash2))

