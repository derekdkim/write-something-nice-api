from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pw_hash(password: str):
    """Hashes a password string into hashed string using bcrypt"""
    return pwd_context.hash(password)

def verify_pw(password: str, hashed_password: str):
    """Validates a plaintext string against hashed password"""
    return pwd_context.verify(password, hashed_password)
