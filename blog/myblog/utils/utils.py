import re

def is_password_valid(password: str) -> bool:
    pattern = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
    return bool(re.fullmatch(pattern, password))