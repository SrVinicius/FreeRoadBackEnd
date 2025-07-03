import uuid
from blog.domain.entities.comment import Comment
from blog.infra.repositories.in_memory_comment_repository import (
    InMemoryCommentRepository,
)
from blog.usecases.comment.add_comment import AddCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase
from blog.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from blog.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase


def create_test_comment(user_id=None, post_id=None) -> Comment:
    return Comment(
        id=str(uuid.uuid4()),
        post_id=post_id or str(uuid.uuid4()),
        user_id=user_id or str(uuid.uuid4()),
        comment="Comentário de teste",
        date="2025-06-09",
    )


def test_add_comment():
    repo = InMemoryCommentRepository()
    comment = create_test_comment()
    usecase = AddCommentUseCase(repo)

    result = usecase.execute(comment)

    assert result == comment
    assert repo._comments[comment.id] == comment


def test_get_comments_by_post():
    repo = InMemoryCommentRepository()
    post_id = str(uuid.uuid4())
    comment1 = create_test_comment(post_id=post_id)
    comment2 = create_test_comment(post_id=post_id)
    comment_other = create_test_comment()

    repo.add_comment(comment1)
    repo.add_comment(comment2)
    repo.add_comment(comment_other)

    usecase = GetCommentsByPostUseCase(repo)
    result = usecase.execute(post_id)

    assert comment1 in result
    assert comment2 in result
    assert comment_other not in result
    assert len(result) == 2


def test_get_comments_by_post_empty():
    repo = InMemoryCommentRepository()
    usecase = GetCommentsByPostUseCase(repo)
    result = usecase.execute("post-vazio")

    assert result == []


def test_get_comments_by_user():
    repo = InMemoryCommentRepository()
    user_id = str(uuid.uuid4())
    comment1 = create_test_comment(user_id=user_id)
    comment2 = create_test_comment(user_id=user_id)
    comment_other = create_test_comment()

    repo.add_comment(comment1)
    repo.add_comment(comment2)
    repo.add_comment(comment_other)

    usecase = GetCommentsByUserUseCase(repo)
    result = usecase.execute(user_id)

    assert comment1 in result
    assert comment2 in result
    assert comment_other not in result
    assert len(result) == 2


def test_get_comments_by_user_empty():
    repo = InMemoryCommentRepository()
    usecase = GetCommentsByUserUseCase(repo)
    result = usecase.execute("user-vazio")

    assert result == []


def test_delete_comment():
    repo = InMemoryCommentRepository()
    comment = create_test_comment()
    repo.add_comment(comment)

    usecase = DeleteCommentUseCase(repo)
    usecase.execute(comment.id)

    assert comment.id not in repo._comments


def test_delete_comment_not_found():
    repo = InMemoryCommentRepository()
    usecase = DeleteCommentUseCase(repo)

    # Só garante que não levanta erro
    usecase.execute("id-invalido")
