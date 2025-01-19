import pyotp
import os

def generate_TOTP():
    secret = os.getenv("VRC_TOTP_SECRET")
    return pyotp.TOTP(secret).now()