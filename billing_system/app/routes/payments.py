from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.logger import logger
from app.database import get_db
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["Payments"]
)
def send_payment_email():
    print("Payment confirmation email sent")
from fastapi import BackgroundTasks

@router.post("/pay/{invoice_id}")
def pay_invoice(
    invoice_id: int,
    payment: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    existing_payment = db.query(Payment).filter(
        Payment.invoice_id == invoice_id
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    if payment.amount != invoice.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Amount must match invoice total"
        )

    new_payment = Payment(
        invoice_id=invoice_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="Success"
    )

    db.add(new_payment)

    invoice.status = "Paid"

    db.commit()
    db.refresh(new_payment)
    logger.info(
    f"Payment successful for invoice {invoice_id}"
)
    background_tasks.add_task(
    send_payment_email
)

    return {
        "message": "Payment successful",
        "payment_id": new_payment.id
    }

@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment

@router.get("/payments")
def get_payments(db: Session = Depends(get_db)):

    payments = db.query(Payment).all()

    return payments

