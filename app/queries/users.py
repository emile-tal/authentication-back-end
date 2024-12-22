from hashlib import sha256
from app.database import get_db_conn, close_db_conn

# TO DO add salt to hashing

def loginUser(username, password):
    conn = get_db_conn()
    with conn.cursor() as cur:
        retrieve_password_query = "SELECT password FROM users WHERE username = %s"
        cur.execute(retrieve_password_query, username)
        saved_password = cur.fetchone()
        if sha256(password.encode('utf-8')).hexdigest() == saved_password:
            print('success')
    close_db_conn()

def registerUser(username, password):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    conn = get_db_conn()
    with conn.cursor() as cur:
        insert_user_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cur.execute(insert_user_query, (username, hashed_password))
        conn.commit()
        close_db_conn()
