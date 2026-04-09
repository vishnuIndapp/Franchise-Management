import random
from app.core.config import settings

OTP_EXPIRATION_SECONDS = settings.OTP_EXPIRATION_SECONDS

def generate_otp():
    otp = f"{random.randint(100000, 999999)}"
    return otp