from app.utils.redis import r
from app.utils.otp import generate_otp, OTP_EXPIRATION_SECONDS
from app.utils.smtp import send_email


def send_otp( email: str) :
    otp = generate_otp()

    r.setex(f"otp:{email}", OTP_EXPIRATION_SECONDS, otp)

    sent=send_email(email, otp)

    return sent

def verify_otp(email: str, otp: str) :
    stored_otp = r.get(f"otp:{email}")

    if not stored_otp:
        return False
    if stored_otp != otp:
        return False
    r.delete(f"otp:{email}")
    return True