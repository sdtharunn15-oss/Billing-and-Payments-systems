from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str


class CustomerSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True