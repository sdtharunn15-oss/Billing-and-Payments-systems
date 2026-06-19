from fastapi import FastAPI
from app.routes.invoices import router as invoice_router
from app.database import Base, engine
from app.routes.customers import router as customer_router
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.payment import Payment
from app.routes.auth import router as auth_router
from app.routes.payments import router as payment_router
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Billing & Payment System"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(payment_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Billing System Running"}


