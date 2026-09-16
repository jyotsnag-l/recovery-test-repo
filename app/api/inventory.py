from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import InventoryItemCreate, InventoryItemResponse, InventoryItemUpdate
from app.services import inventory_service

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


@router.post("/", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_in: InventoryItemCreate, db: Session = Depends(get_db)):
    return inventory_service.create_inventory_item(db, item_in)


@router.get("/{item_id}", response_model=InventoryItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return inventory_service.get_inventory_item(db, item_id)


@router.get("/", response_model=List[InventoryItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return inventory_service.get_all_inventory_items(db, skip=skip, limit=limit)


@router.patch("/{item_id}/stock", response_model=InventoryItemResponse)
def update_stock(item_id: int, update_in: InventoryItemUpdate, db: Session = Depends(get_db)):
    return inventory_service.update_inventory_stock(db, item_id, update_in)
