# from app.migrations.migrations import migrate_user_tables, migrate_sessions_tables

# migrate_user_tables()
# migrate_sessions_tables()


import secrets
from cryptography.fernet import Fernet
import base64

# Generate the keys
signing_key = secrets.token_bytes(32)  # 32 bytes
encryption_key = Fernet.generate_key()  # Fernet generates a base64-encoded key

# Encode the signing key to Base64 for storage
encoded_signing_key = base64.b64encode(signing_key).decode()

print("SIGNING_KEY for .env:", encoded_signing_key)
print("ENCRYPTION_KEY for .env:", encryption_key.decode())