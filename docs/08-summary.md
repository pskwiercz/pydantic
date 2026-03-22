# Summary

Key learnings and next steps.

## What you learned

This crash course covered the essential 80/20 of Pydantic:

**Chapter 1: Introduction**
- Python's dynamic typing causes runtime errors with external data
- Pydantic validates data at runtime and gives clear error messages
- Pydantic is the foundation of modern Python frameworks like FastAPI

**Chapter 2: Type Hints**
- Type hints document what types your code expects
- Basic types: `str`, `int`, `float`, `bool`
- Container types: `list[str]`, `dict[str, int]`
- Optional values: `str | None`
- Literal types for specific allowed values

**Chapter 3: Your First Model**
- `BaseModel` is the core building block
- Fields are defined with type hints
- `model_dump()` converts to dict, `model_validate()` creates from dict
- Dataclasses don't validate, Pydantic does

**Chapter 4: Validation and Fields**
- `Field()` adds constraints: `min_length`, `max_length`, `gt`, `ge`, `lt`, `le`
- Pydantic coerces compatible types automatically
- Validation errors are human-readable and include field locations
- `model_json_schema()` generates JSON Schema for API docs

**Chapter 5: Nested Models**
- Models can contain other models
- Lists of models: `list[OrderItem]`
- Pydantic validates nested data recursively
- `model_dump()` converts the entire tree

**Chapter 6: Pydantic Settings**
- `BaseSettings` reads from environment variables automatically
- Field names map to uppercase env vars
- Supports `.env` files with `SettingsConfigDict`
- `SecretStr` hides sensitive values from logs

**Chapter 7: Structured Output**
- LLMs return text, but you need structured data
- Define response schemas as Pydantic models
- Validation errors enable retry mechanisms
- Works with OpenAI, Anthropic, and other providers

## Key patterns

```python
from pydantic import BaseModel, Field

# Define a model
class User(BaseModel):
    name: str = Field(min_length=1)
    email: str
    age: int | None = None

# Create from data
user = User(name="Alice", email="alice@example.com")

# Convert to dict
data = user.model_dump()

# Create from dict (validation)
user = User.model_validate({"name": "Bob", "email": "bob@example.com"})
```

## Next steps

**Practice on your own:**
- Add Pydantic models to an existing project
- Replace raw dictionaries with validated models
- Use `pydantic-settings` for your configuration

## Build production AI systems

Pydantic is one piece of the puzzle. If you want to learn how to build complete AI systems, check out the [GenAI Accelerator](https://academy.datalumina.com/accelerator).

It's a 6-week program that covers everything from Pydantic and FastAPI to RAG pipelines, LLM monitoring, and deployment.

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Python for AI](https://python.datalumina.com)

[Back to course overview](../README.md)
