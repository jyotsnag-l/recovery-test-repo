def test_create_successful_order(client):
    # 1. Create item
    item_resp = client.post("/api/v1/inventory/", json={
        "sku": "MONITOR-001",
        "name": "4K Monitor",
        "price": 350.00,
        "stock_quantity": 5
    })
    item_id = item_resp.json()["id"]

    # 2. Create order for 2 units
    order_payload = {
        "customer_email": "buyer@example.com",
        "items": [
            {"inventory_item_id": item_id, "quantity": 2}
        ]
    }
    order_resp = client.post("/api/v1/orders/", json=order_payload)
    assert order_resp.status_code == 201
    order_data = order_resp.json()
    assert order_data["status"] == "COMPLETED"
    assert order_data["total_amount"] == 700.00

    # 3. Check that inventory stock was reduced to 3
    inv_resp = client.get(f"/api/v1/inventory/{item_id}")
    assert inv_resp.json()["stock_quantity"] == 3
