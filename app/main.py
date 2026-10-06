from fastapi import FastAPI
from app.database import Base, engine
from app.api import inventory, orders
# pyrefly: ignore [missing-import]
from recovery_sdk.integrations.fastapi import RecoveryMiddleware

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Order Management API",
    description="Backend API service for managing inventory items and customer orders.",
    version="1.0.0"
)

app.include_router(inventory.router)
app.include_router(orders.router)

app.add_middleware(
    RecoveryMiddleware,
    project_id="proj_04102d07",        # your project ID from the platform
    environment="production",
    api_url="http://127.0.0.1:8000" # your Overmend API
)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Inventory & Order Management API is running"}

# This method is to simulate what happens when an exception occurs
@app.get("/test-error")
def test_error():
    raise ValueError("Testing Overmend SDK integration!") 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)

