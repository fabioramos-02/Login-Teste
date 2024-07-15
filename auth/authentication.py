from crud import get_user_by_username

def authenticate_user(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if user and user['password'] == password:
        return True
    return False
