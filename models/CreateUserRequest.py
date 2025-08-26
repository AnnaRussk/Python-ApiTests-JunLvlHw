from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str