from pydantic import BaseModel, Field
from typing import Optional


class PostCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    user_id: str = Field(..., description="ID do usuário que está postando")
    date: str = Field(..., description="Data de criação do post")


class PostUpdateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")


class PostOutput(BaseModel):
    id: str = Field(..., description="ID do post")
    title: str = Field(..., min_length=3, max_length=100, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    user_id: str = Field(..., description="ID do usuário que está postando")
    date: str = Field(..., description="Data de criação do post")

    @classmethod
    def from_entity(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            description=post.description,
            content=post.content,
            user_id=post.user_id,
            date=post.date,
        )
