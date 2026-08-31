from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    password_hash_value: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        password_hash_value,
    )