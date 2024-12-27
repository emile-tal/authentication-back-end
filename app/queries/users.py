from hashlib import sha256
from app.database import get_db_conn, close_db_conn

def login_user(email, password):
    try:
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
    except Exception as err:
        print(f'Error logging in: {err}')
        return None

def is_email_unique(email):
    try:
        conn = get_db_conn()
        with conn.cursor() as cur:
            find_same_email_query = "SELECT email FROM users WHERE email = %s"
            cur.execute(find_same_email_query, (email,))
            user = cur.fetchone()
            return user is None
    except Exception as err:
        print(f'Error verifying user email: {err}')
        return False

def register_user(email, password, first_name, last_name):
    try:
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        conn = get_db_conn()
        with conn.cursor() as cur:
            insert_user_query = "INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id"
            cur.execute(insert_user_query, (email, hashed_password, first_name, last_name))
            user_id = cur.fetchone()['id']
            conn.commit()
            close_db_conn(conn)
            return user_id
    except Exception as err:
        print(f"Error registering user: {err}")
        return None

def get_user_name(id):
    try:
        conn = get_db_conn()
        with conn.cursor() as cur:
            get_user_name_query = "SELECT first_name FROM users WHERE id = %s"
            cur.execute(get_user_name_query, id)
            user_name = cur.fetchone()['first_name']
            close_db_conn(conn)
            return user_name
    except Exception as err:
        print(f"Error retrieving user's name: {err}")
        return None
