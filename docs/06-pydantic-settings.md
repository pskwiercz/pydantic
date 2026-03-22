# Pydantic Settings

Type-safe configuration from environment variables

## The problem with environment variables

Environment variables are strings. Always:

```python
import os

api_key = os.getenv("API_KEY")           # str | None
max_connections = os.getenv("MAX_CONNECTIONS")  # str | None - not an int!
debug_mode = os.getenv("DEBUG")          # str | None - not a bool!
```

You have to manually:
- Check if values exist
- Convert types
- Validate values
- Handle defaults

This leads to bugs. Pydantic Settings solves this.

## Installation

Pydantic Settings is a separate package. Add it to your project:

```bash
uv add pydantic-settings
```

If you're following this course, it's already installed via `uv sync`.

## Your first settings class

Create a settings class that reads from environment variables:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    max_connections: int = 100
    debug: bool = False

# Reads from environment variables automatically
settings = Settings()

print(settings.api_key)           # From API_KEY env var
print(settings.max_connections)   # From MAX_CONNECTIONS or default 100
print(settings.debug)             # From DEBUG or default False
```

Set environment variables in your shell:

```bash
export API_KEY="sk-abc123"
export MAX_CONNECTIONS="200"
export DEBUG="true"
```

Then run your Python code. Pydantic reads and validates them automatically.

## How it works

Pydantic Settings maps field names to environment variables:

| Field name | Environment variable |
|------------|---------------------|
| `api_key` | `API_KEY` |
| `max_connections` | `MAX_CONNECTIONS` |
| `database_url` | `DATABASE_URL` |

Field names are converted to uppercase for the environment variable lookup.

## Type conversion

Pydantic Settings handles type conversion automatically:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int              # "8080" -> 8080
    debug: bool            # "true" -> True
    rate_limit: float      # "1.5" -> 1.5
    allowed_hosts: list[str]  # "host1,host2" -> ["host1", "host2"]
```

Boolean values accept: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`

## Loading from .env files

Store environment variables in a `.env` file:

```
# .env
API_KEY=sk-abc123
DATABASE_URL=postgresql://localhost/mydb
DEBUG=true
MAX_CONNECTIONS=200
```

Configure your settings to read from it:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    api_key: str
    database_url: str
    debug: bool = False
    max_connections: int = 100

settings = Settings()
print(settings.api_key)  # sk-abc123
```

The `model_config` tells Pydantic where to find the `.env` file.

## Environment variable prefix

Add a prefix to avoid naming conflicts:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MYAPP_")
    
    api_key: str
    debug: bool = False

# Now reads from MYAPP_API_KEY and MYAPP_DEBUG
settings = Settings()
```

Your `.env` file:

```
MYAPP_API_KEY=sk-abc123
MYAPP_DEBUG=true
```

## Handling secrets

Use `SecretStr` for sensitive values:

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: SecretStr
    database_password: SecretStr

settings = Settings()

# Secrets are hidden when printed
print(settings.api_key)  # **********

# Access the actual value when needed
actual_key = settings.api_key.get_secret_value()
```

This prevents accidental logging of sensitive data.

## Real-world example

A complete settings class for a web application:

```python
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )

    # API Configuration
    api_key: SecretStr
    api_base_url: str = "https://api.example.com"
    request_timeout: int = Field(default=30, ge=1, le=300)

    # Database
    database_url: str
    max_connections: int = Field(default=10, ge=1, le=100)

    # Application
    debug: bool = False
    log_level: str = "INFO"

# Usage
settings = Settings()

print(f"API URL: {settings.api_base_url}")
print(f"Timeout: {settings.request_timeout}s")
print(f"Debug mode: {settings.debug}")
```

Your `.env` file:

```
API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:pass@localhost/mydb
DEBUG=true
LOG_LEVEL=DEBUG
```

## Validation works too

All Pydantic validation applies to settings:

```python
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = Field(ge=1, le=65535)
    max_connections: int = Field(ge=1, le=1000)
    timeout_seconds: float = Field(gt=0)

# Invalid values in environment variables will raise ValidationError
```

## Nested settings

For complex configuration:

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")
    
    debug: bool = False
    database: DatabaseSettings = DatabaseSettings()

# Set via: DATABASE__HOST, DATABASE__PORT, DATABASE__NAME
settings = Settings()
```

## Common patterns

### Singleton settings

Load settings once and reuse:

```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Use throughout your app
settings = get_settings()
```

### Environment-specific settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    environment: str = "development"
    debug: bool = False
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

settings = Settings()
if settings.is_production:
    # Production-specific behavior
    pass
```

## Learn more

- [Pydantic Settings documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [pydantic-settings on GitHub](https://github.com/pydantic/pydantic-settings)

## What's next?

You now know how to manage configuration safely. In the final chapter, we'll see how Pydantic works with LLMs to get structured output.

[Next: Structured LLM Output](07-structured-llm-output.md)
