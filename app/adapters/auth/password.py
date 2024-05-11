from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash((BcryptHasher(),))


class PasswordProcessor:
    def verify_password(self, plain_password: str | bytes, hashed_password: str | bytes):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str | bytes):
        return pwd_context.hash(password)
