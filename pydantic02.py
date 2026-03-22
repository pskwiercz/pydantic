from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated
from pydantic import BaseModel, ValidationError, Field

"""
Pydantic built-in types: https://docs.pydantic.dev/latest/api/types/#pydantic.types
"""
class User(BaseModel):
    uid: int | str
    username: str
    email: str
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None


user = User(uid="123",
            username='tom',
            email='tom@google.com')

print(user.model_dump_json(indent=2))

try:
    user = User(uid="123",
                username=['ada'],
                email='tom@google.com')
except ValidationError as e:
    print(e)


# Field
class BlogPost(BaseModel):
    title: str
    content: str
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    # Why default_factory and lambda - in other case all BlogPost will have SAME DATE - because default_factory
    # is invoked once during class compilation
    create_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC))  # or Field(default_factory=partial(datetime.now, tz=UTC))
    author_id: str | int
    status: Literal["draft", "published", "archived"] = "draft"


post = BlogPost(
    title="First Blog",
    content="First sentence",
    author_id="123"
)

print(post.model_dump_json(indent=2))


# Annotated
class UserAnnotated(BaseModel):
    uid: Annotated[int, Field(gt=0)]
    username: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(gt=13, lt=130)]
    email: str
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None


user = UserAnnotated(uid=123,
                     username='tom',
                     age=15,
                     email='tom@google.com')

print(user.model_dump_json(indent=2))

class BlogPostAnnotated(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10, max_length=200)]
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    create_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC))
    author_id: str | int
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z][0-9-]+$")]


post = BlogPostAnnotated(
    title="First Blog",
    content="First sentence",
    author_id="123",
    slug="s1-20"
)

print(post.model_dump_json(indent=2))
