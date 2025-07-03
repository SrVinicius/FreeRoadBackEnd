import uuid
from blog.domain.entities.post import Post
from blog.infra.repositories.in_memory_post_repository import InMemoryPostRepository
from blog.usecases.post.create_post import CreatePostUseCase
from blog.usecases.post.delete_post import DeletePostUseCase
from blog.usecases.post.get_all_posts import GetAllPostsUseCase
from blog.usecases.post.get_post_by_id import GetPostByIdUseCase
from blog.usecases.post.update_post import UpdatePostUseCase


def create_test_post() -> Post:
    return Post(
        id=str(uuid.uuid4()),
        title="Título de Exemplo",
        description="Descrição de Exemplo",
        content="Conteúdo do post",
        user_id=str(uuid.uuid4()),
        date="2025-06-09",
    )


def test_create_post():
    repo = InMemoryPostRepository()
    usecase = CreatePostUseCase(repo)
    post = create_test_post()

    result = usecase.execute(post)

    assert result == post
    assert repo.get_by_id(post.id) == post


def test_get_all_posts():
    repo = InMemoryPostRepository()
    post1 = create_test_post()
    post2 = create_test_post()
    repo.create(post1)
    repo.create(post2)

    usecase = GetAllPostsUseCase(repo)
    result = usecase.execute()

    assert len(result) == 2
    assert post1 in result
    assert post2 in result


def test_get_post_by_id():
    repo = InMemoryPostRepository()
    post = create_test_post()
    repo.create(post)

    usecase = GetPostByIdUseCase(repo)
    result = usecase.execute(post.id)

    assert result == post


def test_get_post_by_id_not_found():
    repo = InMemoryPostRepository()
    usecase = GetPostByIdUseCase(repo)
    result = usecase.execute("id-invalido")

    assert result is None


def test_update_post():
    repo = InMemoryPostRepository()
    post = create_test_post()
    repo.create(post)

    updated = Post(
        id=post.id,
        title="Título Atualizado",
        description="Descrição Atualizada",
        content="Novo conteúdo",
        user_id=str(uuid.uuid4()),
        date="2025-06-10",
    )

    usecase = UpdatePostUseCase(repo)
    result = usecase.execute(updated)

    assert result.title == "Título Atualizado"
    assert repo.get_by_id(post.id).content == "Novo conteúdo"


def test_update_post_not_found():
    repo = InMemoryPostRepository()
    post = create_test_post()

    usecase = UpdatePostUseCase(repo)
    result = usecase.execute(post)

    assert result is None


def test_delete_post():
    repo = InMemoryPostRepository()
    post = create_test_post()
    repo.create(post)

    usecase = DeletePostUseCase(repo)
    usecase.execute(post.id)

    assert repo.get_by_id(post.id) is None


def test_delete_post_not_found():
    repo = InMemoryPostRepository()
    usecase = DeletePostUseCase(repo)

    # Apenas garantir que não levanta exceção
    usecase.execute("id-invalido")
