from fastapi import FastAPI
from app.database import Base, engine
from app.api import inventory, orders

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Order Management API",
    description="Backend API service for managing inventory items and customer orders.",
    version="1.0.0"
)

app.include_router(inventory.router)
app.include_router(orders.router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Inventory & Order Management API is running"}
