import sqlite3
import contextlib
from http import HTTPStatus
from helpers.constants import ROLE
from helpers.response import raise_exception
from random import choice
from models import *
from helpers.response import *

def get_user_by_username(username: str, db: sqlite3.Connection, hide_password: bool = True):
    sql = """
    SELECT 
    user.id as user_id,
    user.username as username,
    user.first_name as first_name,
    user.last_name as last_name,
    user.password as password,
    role.name as role
    FROM user
    LEFT JOIN user_role
    ON user_role.user_id = user_id
    LEFT JOIN role
    ON user_role.user_id.role_id = role_id
    WHERE user.username = ?
    """
    get_user = db.execute(sql, [username]).fetchall()

    if get_user:
        user = {
            "user_id" : get_user[0]["user_id"],
            "username": get_user[0]["username"],
            "first_name":get_user[0]["first_name"],
            "last_name":get_user[0]["last_name"],
            "role":[get_user[0]["role"]]
        }
        if not hide_password:
            user["passsword"] = get_user[0]["password"]

        for x in range(1, len(get_user)):
            user["role"].append(get_user[x]["role"])

        return user
    return None

def gracefully_handle_db_transaction(sql:str, db: sqlite3.Connection):
    try:
        db.executescript(sql)
        db.commit()
        return True
    except sqlite3.IntegrityError as e:
        db.rollback()
        raise_exception(status_code=HTTPStatus.CONFLICT, message =str(e))

def create_user_sql_script(user: NewAccountRequest):
    sql_script = f'''
    INSERT INTO "user" (username, first_name, last_name, password)
    VALUES ("{user.username}", "{user.first_name}","{user.last_name}","{hash_password(user.password)}");
    '''
    for role in user.role:
        sql_script += f'''
        INSERT INTO "user_role" (user_id, role_id)
        VALUES ((SELECT id FROM "user" WHERE username = "{user.username}"), {ROLE[role]});
        '''

    return sql_script