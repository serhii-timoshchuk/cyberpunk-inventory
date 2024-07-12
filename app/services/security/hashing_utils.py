from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Returns the password hash"""
    return pwd_context.hash(str(password))


def verify_password(plain_password, hashed_password) -> bool:
    """Returns True if the password is correct, False otherwise"""
    return pwd_context.verify(plain_password, hashed_password)
