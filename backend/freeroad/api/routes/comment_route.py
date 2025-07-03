from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from freeroad.api.deps import comment_repo
from freeroad.usecases.comment.add_comment import AddCommentUseCase
from freeroad.usecases.comment.delete_comment import DeleteCommentUseCase
from freeroad.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from freeroad.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase
from freeroad.domain.entities.comment import Comment
import uuid
from freeroad.api.schemas.comment_schema import AddCommentInput, CommentOutput

router = APIRouter()


@router.get("/post/{post_id}", response_model=CommentOutput)
def get_comments_by_post(post_id: str):
    usecase = GetCommentsByPostUseCase(comment_repo)
    comments = usecase.execute(post_id)
    return comments


@router.get("/user/{user_id}", response_model=CommentOutput)
def get_comments_by_user(user_id: str):
    usecase = GetCommentsByUserUseCase(comment_repo)
    comments = usecase.execute(user_id)
    return comments


@router.post("/", response_model=CommentOutput)
def add_comment(data: AddCommentInput):
    comment = Comment(
        id=str(uuid.uuid4()),
        post_id=data.post_id,
        user_id=data.user_id,
        comment=data.comment,
        date=data.date,
    )
    usecase = AddCommentUseCase(comment_repo)
    added_comment = usecase.execute(comment)
    return added_comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: str):
    usecase = DeleteCommentUseCase(comment_repo)
    success = usecase.execute(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
