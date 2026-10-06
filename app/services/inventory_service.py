from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import InventoryItem
from app.schemas import InventoryItemCreate, InventoryItemUpdate


def create_inventory_item(db: Session, item_in: InventoryItemCreate) -> InventoryItem:
    existing = db.query(InventoryItem).filter(InventoryItem.sku == item_in.sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Inventory item with SKU '{item_in.sku}' already exists."
        )
    item = InventoryItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_inventory_item(db: Session, item_id: int) -> InventoryItem:
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found."
        )
    return item


def get_all_inventory_items(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
    return db.query(InventoryItem).offset(skip).limit(limit).all()


def update_inventory_stock(db: Session, item_id: int, update_in: InventoryItemUpdate) -> InventoryItem:
    item = get_inventory_item(db, item_id)
    item.stock_quantity = update_in.stock_quantity
    db.commit()
    db.refresh(item)
    return item


def validate_stock_availability(db: Session, item_id: int, requested_quantity: int) -> InventoryItem:
    item = get_inventory_item(db, item_id)
    if item.stock_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_204_BAD_REQUEST,
            detail=f"Insufficient stock for item '{item.name}'. Available: {item.stock_quantity}, Requested: {requested_quantity}."
        )
    return item



def deduct_stock(db: Session, item_id: int, quantity: int) -> InventoryItem:
    item = get_inventory_item(db, item_id)
    item.stock_quantity -= quantity
    db.commit()
    db.refresh(item)
    return item
