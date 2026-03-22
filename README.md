# Pydantic Crash Course

Type-safe Python development.

## What you'll learn

Learn Pydantic from scratch and start building type-safe Python applications. This crash course covers the essential 80/20 of Pydantic.

- **Understand the problem** - Why Python's dynamic typing breaks things
- **Type hints** - The foundation Pydantic builds on
- **Data models** - Define and validate your data structures
- **Configuration** - Type-safe settings from environment variables
- **Structured output** - Parse and validate data from external APIs

## Course chapters

| Chapter | Topic | Description |
|---------|-------|-------------|
| 1 | [Introduction](docs/01-introduction.md) | The problem Pydantic solves |
| 2 | [Type Hints](docs/02-type-hints.md) | Python's type system basics |
| 3 | [Your First Model](docs/03-your-first-model.md) | BaseModel fundamentals |
| 4 | [Validation and Fields](docs/04-validation-and-fields.md) | Control what data is acceptable |
| 5 | [Nested Models](docs/05-nested-models.md) | Handle complex data structures |
| 6 | [Pydantic Settings](docs/06-pydantic-settings.md) | Configuration management |
| 7 | [Structured Output](docs/07-structured-llm-output.md) | Parse and validate external data |
| 8 | [Summary](docs/08-summary.md) | Key learnings and next steps |

## Prerequisites

This course assumes you know basic Python:

- Variables and data types
- Functions and classes
- Dictionaries and lists
- Working with APIs

If you need a refresher, check out the [Python course](https://python.datalumina.com).

## Getting started

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

1. Clone this repository

2. Install uv (if you haven't already):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Create environment and install dependencies:

```bash
uv sync
```

4. Run Python files with uv:

```bash
uv run python main.py
```

5. Start with [Chapter 1: Introduction](docs/01-introduction.md)

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Python for AI Course](https://python.datalumina.com)
