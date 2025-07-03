import pytest
from blog.domain.entities.user import User
from blog.domain.entities.post import Post
from blog.domain.entities.comment import Comment
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User("1", "User", email, pwd, "user")
    assert user.name == "User"


def test_invalid_role():
    with pytest.raises(ValueError):
        User("1", "User", Email("user@example.com"), Password("Secret@123"), "invalid")


def test_create_post():
    post = Post("1", "Title", "Desc", "Content", "user_id", "2024-01-01")
    assert post.title == "Title"


def test_create_comment():
    comment = Comment("1", "post1", "user1", "Nice post!", "2024-01-01")
    assert comment.comment == "Nice post!"
