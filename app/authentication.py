import os
import secrets
import hmac
import hashlib
import base64
import re
from time import time
from datetime import datetime
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from app.database import supabase

load_dotenv()

signing_key = base64.b64decode(os.environ["SIGNING_KEY"])
encryption_key = os.environ["ENCRYPTION_KEY"].encode()
cipher = Fernet(encryption_key)

def create_session(user_id):
    try:
        session_id = secrets.token_hex(32)
        session_encrypted = cipher.encrypt(session_id.encode())
        signature = hmac.new(signing_key, session_encrypted, hashlib.sha256).digest()
        signed_cookie = base64.b64encode(session_encrypted + b"." + signature).decode()
        expiry_time = time() + 3600
        expiry_time_formatted = datetime.fromtimestamp(expiry_time)
        response = (
            supabase.table("sessions")
            .insert({"session_id": session_id, "user_id": user_id, "expires_at": str(expiry_time_formatted)})
            .execute()
            )
        return signed_cookie
    except Exception as err:
        (f"Error creating session: {err}")
        return None

def validate_session(session_cookie):
    try:
        data = base64.b64decode(session_cookie.encode())
        session_encrypted, signature = data.rsplit(b".", 1)
        expected_signature = hmac.new(signing_key, session_encrypted, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_signature, signature):
            return None
        session_id = cipher.decrypt(session_encrypted).decode()
        current_time = datetime.fromtimestamp(time())
        valid_session = (
            supabase.table("sessions")
            .select("*")
            .eq("session_id", session_id)
            .gt("expires_at", current_time)
            .execute()
        )
        if len(valid_session.data) > 0:
            expiry_time = time() + 3600
            expiry_time_formatted = datetime.fromtimestamp(expiry_time)
            response = (
                supabase.table("sessions")
                .update({"expires_at", str(expiry_time_formatted)})
                .eq("session_id", session_id)
                .execute()
            )
            return valid_session.data[0]["user_id"]
    except Exception as err:
        (f"Error validating session: {err}")
        return None

def is_email_valid(email):
    email_regex_pattern = r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(email_regex_pattern, email)
