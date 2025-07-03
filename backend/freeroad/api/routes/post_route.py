from fastapi import APIRouter, HTTPException
from freeroad.api.deps import post_repo
from freeroad.usecases.post.create_post import CreatePostUseCase
from freeroad.usecases.post.delete_post import DeletePostUseCase
from freeroad.usecases.post.get_all_posts import GetAllPostsUseCase
from freeroad.usecases.post.get_post_by_id import GetPostByIdUseCase
from freeroad.usecases.post.update_post import UpdatePostUseCase
from freeroad.domain.entities.post import Post
import uuid
from freeroad.api.schemas.post_schema import PostOutput, PostCreateInput, PostUpdateInput

router = APIRouter()


@router.get("/", response_model=PostOutput)
def get_all_posts():
    usecase = GetAllPostsUseCase(post_repo)
    posts = usecase.execute()
    return posts


@router.get("/{post_id}", response_model=PostOutput)
def get_post_by_id(post_id: str):
    usecase = GetPostByIdUseCase(post_repo)
    post = usecase.execute(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostOutput)
def create_post(data: PostCreateInput):
    post = Post(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=data.user_id,
        date=data.date,
    )
    usecase = CreatePostUseCase(post_repo)
    created_post = usecase.execute(post)
    return created_post


@router.put("/{post_id}", response_model=PostOutput)
def update_post(post_id: str, data: PostUpdateInput):
    usecase_get = GetPostByIdUseCase(post_repo)
    existing_post = usecase_get.execute(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = Post(
        id=post_id,
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=existing_post.user_id,
        date=existing_post.date,
    )
    usecase_update = UpdatePostUseCase(post_repo)
    result = usecase_update.execute(updated_post)
    return result


@router.delete("/{post_id}")
def delete_post(post_id: str):
    usecase = DeletePostUseCase(post_repo)
    success = usecase.execute(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
