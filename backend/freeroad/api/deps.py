from blog.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from blog.infra.repositories.in_memory_post_repository import InMemoryPostRepository
from blog.infra.repositories.in_memory_comment_repository import (
    InMemoryCommentRepository,
)

# Instâncias em memória para simulação
user_repo = InMemoryUserRepository()
post_repo = InMemoryPostRepository()
comment_repo = InMemoryCommentRepository()
