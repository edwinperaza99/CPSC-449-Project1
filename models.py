from pydantic import BaseModel

#User roles (Porject 2)

class NewAccountRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: list[str]

class LoginRequest(BaseModel):
    username:str
    password:str

class Response(BaseModel):
    status: int
    message: str
    data: list | dict