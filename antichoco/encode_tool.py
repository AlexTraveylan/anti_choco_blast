import bcrypt


def generate_hash(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


encoded = generate_hash("1234")
print(check_password("1234", encoded))  # True
