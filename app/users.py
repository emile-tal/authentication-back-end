from hashlib import sha256
from app.database import supabase

def login_user(email, password):
    try:
        user = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )
        if len(user.data) > 0:
            if sha256(password.encode('utf-8')).hexdigest() == user.data[0]["password"]:
                return user.data[0]["id"]
        return None
    except Exception as err:
        print(f'Error logging in: {err}')
        return None

def register_user(email, password, first_name, last_name):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    try:
        user = (
            supabase.table("users")
            .insert({"first_name": first_name, "last_name": last_name, "email": email, "password": hashed_password})
            .execute()
        )
        return user.data[0]["id"]
    except Exception as err:
        print(f"Error registering user: {err}")
        return None

def get_user_name(id):
    try:
        user = (
            supabase.table("users")
            .select("*")
            .eq("id", id)
            .execute()
        )
        return user.data[0]["first_name"]
    except Exception as err:
        print(f"Error retrieving user's name: {err}")
        return None
