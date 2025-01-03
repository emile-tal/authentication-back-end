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
from app.database import get_db_conn, close_db_conn

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
        conn = get_db_conn()
        with conn.cursor() as cur:
            insert_session_query = "INSERT INTO sessions (session_id, user_id, expires_at) VALUES (%s, %s, %s)"
            cur.execute(insert_session_query, (session_id, user_id, expiry_time_formatted))
            conn.commit()
            close_db_conn(conn)
        return signed_cookie
    except Exception as err:
        print(f"Error creating session: {err}")
        return None

def validate_session(session_cookie):
    try:
        data = base64.b64decode(session_cookie.encode())
        session_encrypted, signature = data.rsplit(b".", 1)
        expected_signature = hmac.new(signing_key, session_encrypted, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_signature, signature):
            return None
        session_id = cipher.decrypt(session_encrypted).decode()
        conn = get_db_conn()
        with conn.cursor() as cur:
            current_time = datetime.fromtimestamp(time())
            get_sessions_query = "SELECT * FROM sessions WHERE (expires_at) > %s AND (session_id) = %s"
            cur.execute(get_sessions_query, (current_time, session_id))
            valid_session = cur.fetchone()
            if valid_session is not None:
                expiry_time = time() + 3600
                expiry_time_formatted = datetime.fromtimestamp(expiry_time)
                update_expiry_query = "UPDATE sessions SET (expires_at) = %s WHERE (session_id) = %s"
                cur.execute(update_expiry_query, (expiry_time_formatted, session_id))
                return valid_session['user_id']
    except Exception as err:
        print(f"Error validating session: {err}")
        return None

def is_email_valid(email):
    email_regex_pattern = r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(email_regex_pattern, email)
