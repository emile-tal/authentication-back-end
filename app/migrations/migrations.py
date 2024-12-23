from app.database import get_db_conn, close_db_conn

def migrate_user_tables():
    conn = get_db_conn()
    with conn.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS sessions')
        cur.execute('DROP TABLE IF EXISTS users')
        create_user_script = '''
            CREATE TABLE users (
            id          SERIAL PRIMARY KEY,
            email       VARCHAR(255) NOT NULL,
            password    VARCHAR(255) NOT NULL )
            '''
        cur.execute(create_user_script)
        conn.commit()
    close_db_conn(conn)

def migrate_sessions_tables():
    conn = get_db_conn()
    with conn.cursor() as cur:
        create_sessions_script = '''
            CREATE TABLE sessions (
            session_id  VARCHAR(255) PRIMARY KEY,
            user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            expires_at  TIMESTAMP NOT NULL )
            '''
        cur.execute(create_sessions_script)
        conn.commit()
    close_db_conn(conn)