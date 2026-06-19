from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    tax = Column(Float, default=0)
    discount = Column(Float, default=0)
    total_amount = Column(Float)
    due_date = Column(Date)

    status = Column(String, default="Pending")

    customer = relationship(
        "Customer",
        back_populates="invoices"
    )

    items = relationship(
    "InvoiceItem",
    back_populates="invoice",
    cascade="all, delete"
)
    
    