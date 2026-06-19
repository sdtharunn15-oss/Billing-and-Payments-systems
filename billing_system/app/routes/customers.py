from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerSchema
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerSchema

router = APIRouter()

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)

@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.get("/")
def get_customers(
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerSchema, db: Session = Depends(get_db)):

    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db_customer.name = customer.name
    db_customer.email = customer.email
    db_customer.phone = customer.phone

    db.commit()
    db.refresh(db_customer)

    return {
        "message": "Customer updated successfully",
        "customer": db_customer
    }

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):

    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }