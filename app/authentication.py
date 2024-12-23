import os
import secrets
import hmac
import hashlib
import base64
from time import time
from datetime import datetime
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from app.database import get_db_conn, close_db_conn

load_dotenv()

signing_key = base64.b64decode(os.environ["SIGNING_KEY"])
encryption_key = os.environ["ENCRYPTION_KEY"].encode()

def create_session(user_id):
    cipher = Fernet(encryption_key)
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
