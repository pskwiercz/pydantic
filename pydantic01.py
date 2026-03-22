from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    age: int

def main():
    user = User(name="Alice", email="alice@example.com", age=30)
    print(f"User: {user.name}")
    print(f"Email: {user.email}")
    print(f"Age: {user.age}")

    user = User(name="Bob", email="aaa", age=10.00)

    print(user.model_dump())
    print(user.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
