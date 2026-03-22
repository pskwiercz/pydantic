# Validation and Fields

Control what data is acceptable.

## Beyond type checking

Pydantic validates types, but you often need more:

- Email must be a valid format
- Age must be positive
- Username must be 3-20 characters
- Price can't be negative

The `Field()` function lets you add these constraints.

## The Field function

Import `Field` from pydantic and use it to add constraints:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, le=120)
    email: str

user = User(name="Alice", age=30, email="alice@example.com")
```

Now `name` must be 1-100 characters, and `age` must be between 1 and 120.

## String constraints

Control string length and format:

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    bio: str = Field(max_length=500)
    website: str = Field(pattern=r"^https?://.*")

# Valid
profile = UserProfile(
    username="alice_dev",
    bio="Python developer",
    website="https://example.com"
)

# Invalid - username too short
profile = UserProfile(username="ab", bio="Hi", website="https://x.com")
# ValidationError: username must be at least 3 characters
```

String constraints:
- `min_length` - Minimum number of characters
- `max_length` - Maximum number of characters
- `pattern` - Regular expression pattern to match

## Numeric constraints

Control number ranges:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)           # Greater than 0
    quantity: int = Field(ge=0)          # Greater than or equal to 0
    discount: float = Field(ge=0, le=1)  # Between 0 and 1

product = Product(
    name="Widget",
    price=29.99,
    quantity=100,
    discount=0.15
)
```

Numeric constraints:
- `gt` - Greater than
- `ge` - Greater than or equal to
- `lt` - Less than
- `le` - Less than or equal to

## Default values with Field

Set defaults while also adding constraints:

```python
from pydantic import BaseModel, Field

class APIConfig(BaseModel):
    api_key: str
    model: str = Field(default="gpt-4")
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=2)

# Only api_key required
config = APIConfig(api_key="sk-abc123")

print(config.model)        # gpt-4
print(config.max_tokens)   # 1000
print(config.temperature)  # 0.7
```

## Field descriptions

Add descriptions for documentation:

```python
from pydantic import BaseModel, Field

class Order(BaseModel):
    order_id: str = Field(description="Unique order identifier")
    total: float = Field(gt=0, description="Order total in USD")
    items: int = Field(ge=1, description="Number of items in order")
```

Descriptions appear in generated JSON schemas and API documentation.

## Custom validators (80/20 overview)

Sometimes built-in constraints aren't enough. Pydantic supports custom validators for business logic:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    
    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        return v.lower()  # Normalize to lowercase

user = User(username="AliceSmith")
print(user.username)  # alicesmith
```

The validator function receives `cls` (the class, since there's no instance yet during validation) and `v` (the value being validated). Return the value to accept it, or raise `ValueError` to reject it.

Custom validators let you:
- Add business-specific validation logic
- Transform values (like normalizing to lowercase)
- Validate things that built-in constraints can't handle

For most cases, built-in constraints and types are enough. Use custom validators only when you need specific business logic.

## Real-world example

Here's a model for a payment form:

```python
from pydantic import BaseModel, Field

class PaymentForm(BaseModel):
    card_number: str = Field(min_length=16, max_length=16)
    expiry_month: int = Field(ge=1, le=12)
    expiry_year: int = Field(ge=2024)
    cvv: str = Field(min_length=3, max_length=4)
    amount: float = Field(gt=0, description="Amount in USD")
    currency: str = Field(default="USD", min_length=3, max_length=3)

payment = PaymentForm(
    card_number="1234567890123456",
    expiry_month=12,
    expiry_year=2025,
    cvv="123",
    amount=99.99
)
```

## Common patterns

### Email validation

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr  # Built-in email validation
```

### URL validation

```python
from pydantic import BaseModel, HttpUrl

class Link(BaseModel):
    url: HttpUrl  # Must be valid HTTP/HTTPS URL
```

### Constrained lists

```python
from pydantic import BaseModel, Field

class Order(BaseModel):
    items: list[str] = Field(min_length=1)  # At least one item
```

## JSON Schema generation

Pydantic can generate JSON Schema from your models. This is useful for API documentation and integration with other tools:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, description="User's full name")
    age: int = Field(ge=0, description="User's age in years")

print(User.model_json_schema())
```

Output:

```python
{
    'properties': {
        'name': {'description': "User's full name", 'minLength': 1, 'type': 'string'},
        'age': {'description': "User's age in years", 'minimum': 0, 'type': 'integer'}
    },
    'required': ['name', 'age'],
    'title': 'User',
    'type': 'object'
}
```

FastAPI uses this to automatically generate API documentation.

## Learn more

- [Fields documentation](https://docs.pydantic.dev/latest/concepts/fields/)
- [Validators documentation](https://docs.pydantic.dev/latest/concepts/validators/)
- [JSON Schema documentation](https://docs.pydantic.dev/latest/concepts/json_schema/)

## What's next?

You know how to validate individual fields. Next, let's learn how to handle complex data with nested models.

[Next: Nested Models](05-nested-models.md)
