import base64
import hashlib
import secrets
import os
import sys
import json
import datetime

ALGORITHM = "pbkdf2_sha256"

def hash_password(password: str, salt=None, iterations=260000):
    if salt is None:
        salt = secrets.token_hex(16)

    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)

def verify_password(password, password_hash):
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = hash_password(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)

def generate_claims(username: str, user_id: int, roles: list):
    expiration_datetime = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=20)
    claims = {
        "aud" : "krakend.local.gd",
        "iss": "auth.local.gd",
        "sub" : username,
        "jti" : str(user_id),
        "roles" : roles,
        "exp" : int(expiration_datetime.timestamp())
    }
    token = {
        "access_token" : claims,
        "refresh_token" : claims,
        "exp" : int(expiration_datetime.timestamp())
    }
    return token
