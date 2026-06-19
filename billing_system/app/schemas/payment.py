from pydantic import BaseModel
from enum import Enum
from fastapi import BackgroundTasks
class PaymentCreate(BaseModel):
    amount: float
    payment_method: str

  

class PaymentMethod(str,Enum):
    UPI = "UPI"
    Card = "Card"
    Wallet = "Wallet"

class PaymentCreate(BaseModel):
    amount: float
    payment_method: PaymentMethod

def send_payment_email():
    print("Payment confirmation email sent")