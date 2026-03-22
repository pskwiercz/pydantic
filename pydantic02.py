from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated
from uuid import UUID, uuid4
from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    EmailStr,
    SecretStr,
    HttpUrl,
    ValidationInfo,
    field_validator,
    model_validator,
    computed_field,
    ConfigDict
)

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

print("---------------------- FIELD ----------------------")
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

print("---------------------- ANNOTATED ----------------------")
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

print("---------------------- BUILT-IN VALIDATORS ----------------------")
# Auto UUDI and Pydantic built-in validators
class UserVal(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: str
    email: EmailStr
    website: HttpUrl | None
    password: SecretStr  # <---- print(user.password.get_secret_value())
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None


user = UserVal(username='tom',
               email='tom@google.com',
               website='http://www.google.com',
               password='aaaaaaaa')

print(user.model_dump_json(indent=2))
print(user.password.get_secret_value())

print("---------------------- CUSTOM VALIDATOR ----------------------")
# Custom validator
class UserVal(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: str
    email: EmailStr
    website: HttpUrl | None
    password: SecretStr  # <---- print(user.password.get_secret_value())
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None

    # Invoked AFTER base validation
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("username must be alphanumeric + underscore")
        else:
            return v.lower()

    # Invoked BEFORE base validation
    @field_validator("website", mode="before")
    @classmethod
    def add_http(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"http://{v}"
        else:
            return v

user = UserVal(username='tom_Tom',
               email='tom@google.com',
               website='www.google.com',
               password='aaaaaaaa')

print(user.model_dump_json(indent=2))

print("---------------------- MODEL VALIDATOR ----------------------")
# Model validator
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self) -> "UserRegistration":
        if self.password != self.confirm_password:
            raise ValueError("Password mismatch")
        return self

try:
    registration = UserRegistration(
        email="tom@gmail.com",
        password="sec123",
        confirm_password="sec12"
    )
    print(registration)
except ValidationError as e:
    print(e)


print("---------------------- COMPUTED FIELD  ----------------------")
# Custom validator
class UserCF(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: str
    email: EmailStr
    website: HttpUrl | None = None
    password: SecretStr  # <---- print(user.password.get_secret_value())
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    username: str | None = None
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 3

user = UserCF(username='tom_Tom',
             email='tom@google.com',
             website='http://www.google.com',
             password='aaaaaaaa',
             )

print(user.model_dump_json(indent=2))

user = UserCF(username='tom_Tom',
              email='tom@google.com',
              website='http://www.google.com',
              password='aaaaaaaa',
              first_name="Adam",
              last_name="Babcki",
              follower_count=4
              )

print(user.model_dump_json(indent=2))

print("---------------------- NESTED TYPES  ----------------------")
class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0

class BlogPostAnnotated(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10, max_length=200)]
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    create_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC))
    status: Literal["draft", "published", "archived"] = "draft"
    author: UserVal
    comments: list[Comment] = Field(default_factory=list)


## BlogPost Dictionary
post_data = {
    "title": "Understanding Pydantic Models",
    "content": "Pydantic makes data validation easy and intuitive...",
    "slug": "understanding-pydantic",
    "author": {
        "username": "coreyms",
        "email": "CoreyMSchafer@gmail.com",
        "age": 39,
        "password": "secret123",
        "website": "http://www.abc.com"
    },
    "comments": [
        {
            "content": "I think I understand nested models now!",
            "author_email": "student@example.com",
            "likes": 25,
        },
        {
            "content": "Can you cover FastAPI next?",
            "author_email": "viewer@example.com",
            "likes": 15,
        },
    ],
}

post = BlogPostAnnotated(**post_data)

print(post.model_dump_json(indent=2))

print("---------------------- ConfigDict  ----------------------")

class UserConfigDict(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uid: UUID = Field(alias="id", default_factory=uuid4) # <------ alias
    username: str
    email: EmailStr
    website: HttpUrl | None = None
    password: SecretStr
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    username: str | None = None
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 3


### User Dictionary
user_data = {
    "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    "username": "Corey_Schafer",
    "email": "CoreyMSchafer@gmail.com",
    "age": "39",
    "password": "secret123",
}
user = UserConfigDict.model_validate(user_data)

print(user.model_dump_json(indent=2)) # <---- UID:

print(user.model_dump_json(indent=2, by_alias=True, exclude={"password"})) # <----  ID & no password

print(user.model_dump_json(indent=2, include={"username", "email"})) # <----  ONLY username and email

