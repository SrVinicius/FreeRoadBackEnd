from pydantic import BaseModel, Field
from typing import Optional


class AddCommentInput(BaseModel):
    post_id: str = Field(
        ..., description="ID do post ao qual o comentário será adicionado"
    )
    user_id: str = Field(..., description="ID do usuário que está comentando")
    comment: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: str = Field(..., description="Data do comentário no formato ISO 8601")


class CommentOutput(BaseModel):
    id: str = Field(..., description="ID do comentário")
    post_id: str = Field(..., description="ID do post ao qual o comentário pertence")
    user_id: str = Field(..., description="ID do usuário que fez o comentário")
    comment: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: str = Field(..., description="Data do comentário no formato ISO 8601")

    @classmethod
    def from_entity(cls, comment):
        return cls(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            comment=comment.comment,
            date=comment.date,
        )
