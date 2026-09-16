from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Order, OrderItem
from app.schemas import OrderCreate
from app.services import inventory_service


def create_order(db: Session, order_in: OrderCreate) -> Order:
    # 1. Validate stock for all items upfront
    items_to_process = []
    for item_in in order_in.items:
        inventory_item = inventory_service.validate_stock_availability(
            db, item_in.inventory_item_id, item_in.quantity
        )
        items_to_process.append((inventory_item, item_in.quantity))

    # 2. Calculate total and reduce stock
    total_amount = 0.0
    order_items = []

    for inventory_item, quantity in items_to_process:
        item_total = inventory_item.price * quantity
        total_amount += item_total

        # Deduct stock in database
        inventory_service.deduct_stock(db, inventory_item.id, quantity)

        order_item = OrderItem(
            inventory_item_id=inventory_item.id,
            quantity=quantity,
            unit_price=inventory_item.price
        )
        order_items.append(order_item)

    # 3. Create Order
    order = Order(
        customer_email=order_in.customer_email,
        status="COMPLETED",
        total_amount=total_amount,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found."
        )
    return order
