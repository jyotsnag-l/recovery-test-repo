def test_create_order_exceeding_stock_should_fail(client):
    # 1. Create item with stock = 3
    item_resp = client.post("/api/v1/inventory/", json={
        "sku": "HEADPHONE-001",
        "name": "Noise Cancelling Headphones",
        "price": 199.99,
        "stock_quantity": 3
    })
    item_id = item_resp.json()["id"]

    # 2. Attempt to order 5 units (exceeds stock of 3)
    order_payload = {
        "customer_email": "eager@example.com",
        "items": [
            {"inventory_item_id": item_id, "quantity": 5}
        ]
    }
    order_resp = client.post("/api/v1/orders/", json=order_payload)
    assert order_resp.status_code == 400
    assert "Insufficient stock" in order_resp.json()["detail"]

    # 3. Ensure stock remains untouched (3)
    inv_resp = client.get(f"/api/v1/inventory/{item_id}")
    assert inv_resp.json()["stock_quantity"] == 3


def test_order_nonexistent_inventory_item_fails(client):
    order_payload = {
        "customer_email": "ghost@example.com",
        "items": [
            {"inventory_item_id": 9999, "quantity": 1}
        ]
    }
    order_resp = client.post("/api/v1/orders/", json=order_payload)
    assert order_resp.status_code == 404
