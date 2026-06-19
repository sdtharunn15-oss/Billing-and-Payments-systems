from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        unique=True
    )

    amount = Column(Float, nullable=False)

    payment_method = Column(String, nullable=False)

    status = Column(String, default="Success")

    invoice = relationship("Invoice")