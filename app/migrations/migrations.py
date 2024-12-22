from app.database import get_db_conn, close_db_conn

def migrate_user_tables():
    conn = get_db_conn()
    with conn.cursor() as cur:
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
