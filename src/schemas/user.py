from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Senha ao criar um novo usuário

class User(UserBase):
    id: int

    class Config:
        orm_mode = True  # Permite que o Pydantic trabalhe com modelos SQLAlchemy