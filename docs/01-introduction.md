# Introduction

Pydantic brings runtime data validation to Python using type hints.

## The problem with Python

Python is dynamically typed. This means you can do this:

```python
age = 25
age = "twenty-five" 
age = ["25", 25, None]
```

No errors. Python doesn't care.

This flexibility is great for quick scripts. But it becomes a nightmare when you're building real applications, especially when working with external data.

## When things go wrong

Imagine you're building an API that receives user data:

```python
def create_user(data):
    user_id = data["id"]
    email = data["email"]
    age = data["age"]
    
    # Later in your code...
    birth_year = 2025 - age  # What if age is "25" instead of 25?
```

Your API receives JSON from the outside world. You expect:

```json
{"id": 1, "email": "dave@example.com", "age": 25}
```

But the API sends:

```json
{"id": 1, "email": null, "age": "unknown"}
```

Your code crashes.

## The real-world impact

In any application, you're constantly working with:

- **API responses** - External services return whatever they want
- **User input** - Never trust user data
- **Configuration** - Environment variables are always strings
- **Database records** - Data can be missing or malformed

Without validation, bugs hide until production. With Pydantic, they surface immediately.

## What Pydantic does

Pydantic validates data at runtime. You define what your data should look like, and Pydantic ensures it matches:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    age: int

# Valid data - works fine
user = User(id=1, email="dave@example.com", age=25)

# Invalid data - fails immediately with clear error
user = User(id=1, email=None, age="unknown")
```

When validation fails, you get a clear error message telling you exactly what went wrong:

```
2 validation errors for User
email
  Input should be a valid string
age
  Input should be a valid integer, unable to parse string as an integer
```

The problem is caught at the source.

## Pydantic in the Python ecosystem

Pydantic is everywhere:

- **FastAPI** uses Pydantic for request/response validation
- **Django Ninja** uses Pydantic for API schemas
- **SQLModel** combines Pydantic with SQLAlchemy
- **Most modern Python frameworks** rely on Pydantic under the hood

Learning Pydantic is about writing reliable, type-safe Python code.

## Installation

Install Pydantic in your project with either `pip` or `uv`:

```bash
pip install pydantic
```

```bash
uv add pydantic
```

## Why learn Pydantic

Next to Python basics, Pydantic is one of the most important libraries to learn. Especially in the era of agentic coding.

- **More robust applications**: Strict Pydantic models catch bugs before they reach production. You define what valid data looks like, and Pydantic enforces it at runtime.
- **AI agents understand your code better**: When you define clear Pydantic models, AI coding assistants can understand your data structures. Models act as guardrails that guide both humans and AI.
- **Required for agentic systems**: Building AI agents that call tools, process data, or interact with APIs? You need structured output. Pydantic models define what the AI should return, making agent responses predictable and type-safe.
- **You'll encounter it everywhere**: If you're interested in Python for AI, you'll run into Pydantic constantly. FastAPI, LangChain, OpenAI SDKs, and most AI frameworks use Pydantic under the hood.

## Learn more

- [Official Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Pydantic on GitHub](https://github.com/pydantic/pydantic)

## What's next?

Before diving deeper into Pydantic, you need to understand type hints. They're the foundation Pydantic builds on.

[Next: Type Hints](02-type-hints.md)
