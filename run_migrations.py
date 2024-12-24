from app.migrations.migrations import migrate_user_tables, migrate_sessions_tables

migrate_user_tables()
migrate_sessions_tables()
