import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), salt=bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password)
