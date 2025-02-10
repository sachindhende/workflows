import hashlib
import logging
from database.db_connector import get_db_connection

logging.basicConfig(filename="logs/auth.log", level=logging.INFO)

ROLE_PERMISSIONS = {
    "admin": {"workflows", "products", "settings", "create_product", "update_product", "delete_product", "view_product"},
    "user": {"workflows", "products", "view_product"},
}

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def authenticate_user(username, password):
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")
        return None, None

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and user["password_hash"] == hash_password(password):
        logging.info(f"Successful login: {username}")
        role = user["role"]
        permissions = ROLE_PERMISSIONS.get(role, set())
        return role, permissions

    logging.warning(f"Failed login attempt: {username}")
    return None, None
