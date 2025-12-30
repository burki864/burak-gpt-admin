ADMINS = ["burak", "admin", "burki864"]

def is_admin(username: str) -> bool:
    return username.lower() in ADMINS
