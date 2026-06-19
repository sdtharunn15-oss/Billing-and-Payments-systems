from pydantic import BaseModel
from datetime import date

class InvoiceItemCreate(BaseModel):
    product_name: str
    quantity: int
    price: float


class InvoiceCreate(BaseModel):
    customer_id: int
    tax: float
    discount: float
    due_date: date
    items: list[InvoiceItemCreate]



from datetime import date
from pydantic import field_validator

@field_validator("due_date")
def validate_due_date(cls, value):
    if value <= date.today():
        raise ValueError("Due date must be future date")
    return value

from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    invoice_number: str
    amount: float
    status: str

    class Config:
        from_attributes = True