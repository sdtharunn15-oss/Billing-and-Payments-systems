from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from fastapi import Query
from app.database import get_db
from app.models.invoice import Invoice
from app.models.customer import Customer
from app.schemas.invoice import InvoiceCreate
from app.schemas.invoice import InvoiceSchema
from app.models.invoice_item import InvoiceItem
from app.services.dependencies import admin_required
router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)

@router.post("/")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    customer = db.query(Customer).filter(
        Customer.id == invoice.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if not customer.is_active:
        raise HTTPException(
            status_code=400,
            detail="Customer inactive"
        )

    subtotal = 0

    for item in invoice.items:
        subtotal += item.quantity * item.price

    total = subtotal + invoice.tax - invoice.discount

    if total <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid total amount"
        )

    db_invoice = Invoice(
        customer_id=invoice.customer_id,
        tax=invoice.tax,
        discount=invoice.discount,
        total_amount=total,
        due_date=invoice.due_date
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.items:

        invoice_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )

        db.add(invoice_item)

    db.commit()

    return {
        "invoice_id": db_invoice.id,
        "total_amount": total
    }


@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
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

    return invoice

@router.get("/")
def get_invoices(
    db: Session = Depends(get_db)
):
    return db.query(Invoice).all()


from datetime import date
from fastapi import Query

@router.get("/")
def get_invoices(
    status: str = None,
    due_date_before: date = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(Invoice)

    if status:
        query = query.filter(
            Invoice.status == status
        )

    if due_date_before:
        query = query.filter(
            Invoice.due_date < due_date_before
        )

    total = query.count()

    invoices = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "page": page,
        "limit": limit,
        "data": invoices
    }

@router.put("/invoices/{invoice_id}")
def update_invoice(
    invoice_id: int,
    invoice: InvoiceSchema,
    db: Session = Depends(get_db)
):

    db_invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not db_invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    db_invoice.invoice_number = invoice.invoice_number
    db_invoice.amount = invoice.amount
    db_invoice.status = invoice.status

    db.commit()
    db.refresh(db_invoice)

    return {
        "message": "Invoice updated successfully",
        "invoice": db_invoice
    }

@router.delete("/invoices/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    db_invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not db_invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    db.delete(db_invoice)
    db.commit()

    return {
        "message": "Invoice deleted successfully"
    }

