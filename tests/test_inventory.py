def test_create_inventory_item(client):
    payload = {
        "sku": "LAPTOP-001",
        "name": "Gaming Laptop",
        "description": "High performance gaming laptop",
        "price": 1299.99,
        "stock_quantity": 10
    }
    response = client.post("/api/v1/inventory/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "LAPTOP-001"
    assert data["name"] == "Gaming Laptop"
    assert data["stock_quantity"] == 10
    assert "id" in data


def test_get_inventory_item(client):
    create_resp = client.post("/api/v1/inventory/", json={
        "sku": "MOUSE-001",
        "name": "Wireless Mouse",
        "price": 25.50,
        "stock_quantity": 50
    })
    item_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/inventory/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Wireless Mouse"


def test_update_inventory_stock(client):
    create_resp = client.post("/api/v1/inventory/", json={
        "sku": "KB-001",
        "name": "Mechanical Keyboard",
        "price": 85.00,
        "stock_quantity": 20
    })
    item_id = create_resp.json()["id"]

    patch_resp = client.patch(f"/api/v1/inventory/{item_id}/stock", json={"stock_quantity": 45})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["stock_quantity"] == 45
