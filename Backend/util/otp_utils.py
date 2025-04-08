import random
import os 
from dotenv import load_dotenv
import redis


load_dotenv()

r = redis.Redis(
    host = "localhost",
    port = 6379,
    db = 0,
    decode_responses=True
)

def genrate_otp():
    return str(random.randint(1000,9999))

def genrate_and_store_otp(email):
    otp = genrate_otp()
    r.setex(f"otp:{email}", 300, otp)

    return otp # Store OTP with a 5-minute expiration

def verify_otp(email:str,otp:str):
    stored_otp = r.get(f"otp:{email}")
    if stored_otp and stored_otp == otp:
        r.delete(f"otp:{email}")
        return True
    return False
