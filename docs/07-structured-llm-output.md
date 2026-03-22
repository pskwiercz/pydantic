# Structured LLM Output

Get type-safe responses from AI models.

## The problem with LLM responses

Large language models return text. Just text:

```python
response = "The product is a laptop. It costs $999. The brand is Apple."
```

But you need structured data:

```python
{
    "product": "laptop",
    "price": 999,
    "brand": "Apple"
}
```

You could parse the text manually. But that's fragile. The model might format things differently next time.

## Structured outputs

Modern LLM APIs support structured outputs. You define a schema, and the model returns data matching that schema. Pydantic is perfect for this.

## OpenAI with Pydantic

OpenAI's API directly supports Pydantic models for structured output:

```python
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class ProductInfo(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool

client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="Extract: The new MacBook Pro costs $1999 and is available now in Electronics.",
    text_format=ProductInfo
)

product = response.output_parsed
print(product.name)      # MacBook Pro
print(product.price)     # 1999.0
print(product.category)  # Electronics
print(product.in_stock)  # True
```

The response is automatically parsed into your Pydantic model.

## Defining extraction schemas

Create models that match what you want to extract:

```python
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: str = Field(description="Full name of the person")
    email: str | None = Field(description="Email address if mentioned")
    phone: str | None = Field(description="Phone number if mentioned")
    company: str | None = Field(description="Company name if mentioned")
```

Descriptions help the LLM understand what to extract.

## Complex extractions

Handle nested and list data:

```python
from datetime import datetime
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ActionItem(BaseModel):
    task: str
    assignee: str | None = None
    due_date: datetime | None = None


class MeetingNotes(BaseModel):
    title: str
    date: datetime
    attendees: list[str]
    summary: str
    action_items: list[ActionItem]
    next_meeting: datetime | None = None


# Use with OpenAI
client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="""
    Meeting: Q1 Planning
    Date: January 15, 2025
    Attendees: Alice, Bob, Charlie
    
    We discussed the roadmap. Alice will prepare the budget by Friday.
    Bob is handling the technical specs. Next sync on January 22.
    """,
    text_format=MeetingNotes,
)

notes = response.output_parsed
print(f"Meeting: {notes.title}")
print(f"Date: {notes.date}")
print(f"Attendees: {', '.join(notes.attendees)}")
for item in notes.action_items:
    print(f"  - {item.task} ({item.assignee})")
```

## Using Literal for constrained outputs

Force the model to choose from specific values:

```python
from typing import Literal
from pydantic import BaseModel

class SentimentAnalysis(BaseModel):
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float

class Classification(BaseModel):
    text: str
    category: Literal["bug", "feature", "question", "other"]
    priority: Literal["low", "medium", "high"]
```

The model can only return values from your defined options.

## Real-world example: Invoice extraction

Extract structured data from unstructured invoice text:

```python
from pydantic import BaseModel, Field
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LineItem(BaseModel):
    description: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor_name: str
    vendor_address: str | None = None
    items: list[LineItem]
    subtotal: float
    tax: float | None = None
    total: float
    payment_status: Literal["paid", "pending", "overdue"] = "pending"


# Extract from invoice text
invoice_text = """
Invoice #INV-2025-001
Date: January 15, 2025
From: Acme Corp, 123 Business St

Items:
- Widget Pro (5) @ $29.99 each
- Service Fee (1) @ $50.00

Subtotal: $199.95
Tax: $16.00
Total: $215.95

Status: Paid
"""

client = OpenAI()
response = client.responses.parse(
    model="gpt-4o", input=f"Extract invoice data:\n{invoice_text}", text_format=Invoice
)

invoice = response.output_parsed
print(f"Invoice: {invoice.invoice_number}")
print(f"From: {invoice.vendor_name}")
print(f"Total: ${invoice.total}")
print(f"Status: {invoice.payment_status}")
```

## Without OpenAI's parsing

If using other LLM providers, request JSON and validate manually:

```python
import json
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float

# Assume you got this JSON string from any LLM
llm_response = '{"name": "Widget", "price": 29.99}'

try:
    data = json.loads(llm_response)
    product = Product.model_validate(data)
    print(f"Valid: {product.name}")
except json.JSONDecodeError:
    print("Invalid JSON from LLM")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Learn more

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

## What's next?

You've completed all the core Pydantic concepts. The final chapter summarizes what you learned and points to next steps.

[Next: Summary](08-summary.md)
