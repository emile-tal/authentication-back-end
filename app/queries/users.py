from hashlib import sha256
from app.database import get_db_conn, close_db_conn

# TO DO add salt to hashing password
# TO DO turn psycopg fetch into dictionary rather than tuple
# TO DO loginuser returns user id rather than true/false

def loginUser(email, password):
    conn = get_db_conn()
    with conn.cursor() as cur:
        retrieve_password_query = "SELECT * FROM users WHERE email = %s"
        cur.execute(retrieve_password_query, (email,))
        user = cur.fetchone()
        close_db_conn(conn)
        return sha256(password.encode('utf-8')).hexdigest() == user[2]

def registerUser(email, password):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    conn = get_db_conn()
    with conn.cursor() as cur:
        insert_user_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cur.execute(insert_user_query, (email, hashed_password))
        conn.commit()
        close_db_conn(conn)
