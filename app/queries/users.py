from hashlib import sha256
from app.database import get_db_conn, close_db_conn

def login_user(email, password):
    conn = get_db_conn()
    with conn.cursor() as cur:
        retrieve_password_query = "SELECT * FROM users WHERE email = %s"
        cur.execute(retrieve_password_query, (email,))
        user = cur.fetchone()
        close_db_conn(conn)
        if user is not None:
            if sha256(password.encode('utf-8')).hexdigest() == user['password']:
                return user['id']
        return None
    
def is_email_unique(email):
    conn = get_db_conn()
    with conn.cursor() as cur:
        find_same_email_query = "SELECT email FROM users WHERE email = %s"
        cur.execute(find_same_email_query, (email,))
        user = cur.fetchone()
        return user is None

def register_user(email, password):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    conn = get_db_conn()
    with conn.cursor() as cur:
        insert_user_query = "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id"
        cur.execute(insert_user_query, (email, hashed_password))
        user_id = cur.fetchone()['id']
        conn.commit()
        close_db_conn(conn)
        return user_id
