from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import secrets
from datetime import datetime, timedelta

app = FastAPI()

otp_store = {}

# Configuration
OTP_EXPIRY_MINUTES = 5
RESEND_DELAY_SECONDS = 60
MAX_ATTEMPTS = 3

class OTPRequest(BaseModel):
    phone_number: str = Field(..., example="+1234567890")

class OTPVerifyRequest(BaseModel):
    phone_number: str = Field(..., example="+1234567890")
    otp: str = Field(..., example="123456")

def generate_otp() -> str:
    """Generate a secure 4-digit OTP."""
    return f"{secrets.randbelow(10**4):04d}"

@app.post("/otp/generate")
def generate_otp_endpoint(request: OTPRequest):
    phone = request.phone_number
    now = datetime.now(datetime.timezone.utc)
    
    # If an OTP already exists for this phone, check the resend delay.
    if phone in otp_store:
        record = otp_store[phone]
        if (now - record["last_sent"]).total_seconds() < RESEND_DELAY_SECONDS:
            raise HTTPException(
                status_code=429, 
                detail="Please wait before requesting a new OTP."
            )
    
    # Generate new OTP and set expiration.
    otp_code = generate_otp()
    expiry = now + timedelta(minutes=OTP_EXPIRY_MINUTES)
    otp_store[phone] = {
        "otp": otp_code,
        "created_at": now,
        "last_sent": now,
        "expiry": expiry,
        "attempts": 0
    }
    
    return {"detail": "OTP generated and sent.", "otp": otp_code}

@app.post("/otp/resend")
def resend_otp(request: OTPRequest):
    phone = request.phone_number
    now = datetime.now(datetime.timezone.utc)
    
    if phone not in otp_store:
        raise HTTPException(
            status_code=404, 
            detail="OTP not found. Please generate an OTP first."
        )
    
    record = otp_store[phone]
    if (now - record["last_sent"]).total_seconds() < RESEND_DELAY_SECONDS:
        raise HTTPException(
            status_code=429, 
            detail="Please wait before resending OTP."
        )
    
    # Generate a new OTP and reset the attempt count.
    otp_code = generate_otp()
    expiry = now + timedelta(minutes=OTP_EXPIRY_MINUTES)
    otp_store[phone].update({
        "otp": otp_code,
        "last_sent": now,
        "expiry": expiry,
        "attempts": 0
    })
    
    return {"detail": "OTP resent.", "otp": otp_code}

@app.post("/otp/verify")
def verify_otp(request: OTPVerifyRequest):
    phone = request.phone_number
    user_otp = request.otp
    now = datetime.now(datetime.timezone.utc)
    
    if phone not in otp_store:
        raise HTTPException(
            status_code=404, 
            detail="OTP not generated for this number."
        )
    
    record = otp_store[phone]
    
    # Check if the OTP has expired.
    if now > record["expiry"]:
        del otp_store[phone]
        raise HTTPException(
            status_code=400, 
            detail="OTP expired, please generate a new OTP."
        )
    
    # Check if the maximum number of attempts has been reached.
    if record["attempts"] >= MAX_ATTEMPTS:
        del otp_store[phone]
        raise HTTPException(
            status_code=403, 
            detail="Too many failed attempts, please generate a new OTP."
        )
    
    # Validate the OTP.
    if user_otp == record["otp"]:
        del otp_store[phone]  # Clean up on successful verification.
        return {"detail": "OTP verified successfully."}
    else:
        otp_store[phone]["attempts"] += 1
        remaining_attempts = MAX_ATTEMPTS - otp_store[phone]["attempts"]
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid OTP. {remaining_attempts} attempt(s) left."
        )
