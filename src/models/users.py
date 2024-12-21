from typing import Optional
from sqlmodel import SQLModel, Field
#from pydantic import BaseModel

#Model de User
class User(SQLModel, table= True):
    id: int = Field(default_factory=None, primary_key=True)
    nome: str = Field(...,alias="Nome")
    username: str = Field(..., alias="Username")
    email: str = Field(..., alias="Email")
    password: str = Field(..., alias="Password")

#Model de resposta de User
class ResponseUser(SQLModel):
    id: int = Field(default_factory=None, primary_key=True)
    nome: str = Field(...,alias="Nome")
    username: str = Field(..., alias="Username")
    email: str = Field(..., alias="Email")