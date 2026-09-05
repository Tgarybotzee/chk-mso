import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Indian Phone Validator")


class PhoneRequest(BaseModel):
    phone: str


def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    phone = re.sub(r"[\s\-().]", "", phone)

    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]

    return phone


def validate_indian_mobile(phone: str):
    normalized = normalize_phone(phone)

    # Indian mobile numbers are normally 10 digits
    # beginning with 6, 7, 8 or 9.
    valid = bool(re.fullmatch(r"[6-9]\d{9}", normalized))

    return {
        "input": phone,
        "normalized": f"+91{normalized}" if valid else None,
        "country": "IN",
        "type": "mobile" if valid else None,
        "valid": valid,
    }


@app.get("/")
def home():
    return {
        "name": "Indian Phone Validator",
        "status": "online",
        "endpoint": "POST /api/check"
    }


@app.post("/api/check")
def check_phone(data: PhoneRequest):
    if not data.phone:
        raise HTTPException(
            status_code=400,
            detail="phone is required"
        )

    return validate_indian_mobile(data.phone)
