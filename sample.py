import OD_backend.sample as sample

plain_password = "Changeme@123"
hashed = sample.hashpw(plain_password.encode('utf-8'), sample.gensalt())
print(hashed.decode())  # Use this string to insert into DB
