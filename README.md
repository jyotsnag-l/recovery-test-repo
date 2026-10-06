# recovery-test-repo

`recovery-test-repo` is a backend test repository designed to test **Overmend AI**, an autonomous software-recovery system. 

It provides a controlled sandbox containing a realistic Python/FastAPI Inventory & Order Management API. The codebase allows introducing controlled, realistic software failures for Overmend AI to detect, analyze, patch, and verify via automated tests and GitHub CI workflows.

---

## Architecture & Tech Stack

- **Python**: 3.11+
- **Framework**: FastAPI
- **ORM & Database**: SQLAlchemy with SQLite
- **Validation**: Pydantic v2
- **Testing**: Pytest & HTTPX TestClient
- **CI/CD**: GitHub Actions

### Repository Structure

```text
app/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── services/
│   ├── __init__.py
│   ├── inventory_service.py
│   └── order_service.py
└── api/
    ├── __init__.py
    ├── inventory.py
    └── orders.py

tests/
├── __init__.py
├── conftest.py
├── test_inventory.py
├── test_orders.py
└── test_order_validation.py

.github/
└── workflows/
    └── tests.yml

requirements.txt
README.md
```

---

## Installation & Setup

1. **Clone the repository** (or navigate to directory):
   ```bash
   cd recovery-test-repo
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the API

Start the FastAPI development server with `uvicorn`:

```bash
uvicorn app.main:app --port 9000 --reload
```

The interactive API documentation (Swagger UI) will be accessible at:
- `http://127.0.0.1:9000/docs`

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

On the `main` branch, all tests pass:
```text
tests/test_inventory.py::test_create_inventory_item PASSED
tests/test_inventory.py::test_get_inventory_item PASSED
tests/test_inventory.py::test_update_inventory_stock PASSED
tests/test_orders.py::test_create_successful_order PASSED
tests/test_order_validation.py::test_create_order_exceeding_stock_should_fail PASSED
tests/test_order_validation.py::test_order_nonexistent_inventory_item_fails PASSED
```

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/inventory/` | Create a new inventory item |
| `GET` | `/api/v1/inventory/{item_id}` | Fetch inventory item by ID |
| `GET` | `/api/v1/inventory/` | List all inventory items |
| `PATCH` | `/api/v1/inventory/{item_id}/stock` | Update item stock quantity |
| `POST` | `/api/v1/orders/` | Place a customer order (validates & reduces stock) |
| `GET` | `/api/v1/orders/{order_id}` | Fetch order details by ID |

---

## GitHub Actions CI Workflow

The workflow `.github/workflows/tests.yml` triggers on `push` and `pull_request` to any branch:
1. Provisions `ubuntu-latest` runner.
2. Installs Python 3.11 and dependencies from `requirements.txt`.
3. Executes `pytest -v`.

---

## Controlled Failure Scenario (`test/failure-inventory-order` branch)

A regression branch named `test/failure-inventory-order` contains a multi-module bug where order validation checks if positive stock exists (`stock_quantity <= 0`) rather than verifying if available stock satisfies the requested order quantity (`stock_quantity < requested_quantity`).

### Reproducing the Failure

1. **Switch to the failure branch**:
   ```bash
   git checkout test/failure-inventory-order
   ```

2. **Execute pytest**:
   ```bash
   pytest
   ```

3. **Expected Failure Output**:
   ```text
   FAILED tests/test_order_validation.py::test_create_order_exceeding_stock_should_fail - AssertionError: assert 201 == 400
   ```
   The order succeeds (`201 Created`) despite requesting 5 items when stock is only 3, causing inventory stock to drop to `-2`.

---

## Exact Commands Reference

### 1. Run the Working Version (`main` branch)
```bash
git checkout main
pytest -v
```

### 2. Create and Switch to the Failure Branch
```bash
git checkout -b test/failure-inventory-order
```

### 3. Run the Failing Tests
```bash
pytest -v
```

### 4. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/recovery-test-repo.git
git push -u origin main
git push -u origin test/failure-inventory-order
```

### 5. Trigger the GitHub Actions CI Failure
Pushing or opening a Pull Request from `test/failure-inventory-order` to `main` on GitHub triggers the GitHub Actions workflow, producing a failed CI run for Overmend AI to process.

---

## Overmend AI Recovery Flow

```text
Developer pushes faulty change to test/failure-inventory-order
                      ↓
          GitHub Actions workflow runs
                      ↓
               Pytest fails in CI
                      ↓
     Overmend receives GitHub Webhook notification
                      ↓
 Overmend fetches repo + CI log output traceback
                      ↓
  Overmend AI agent analyzes root cause & writes fix
                      ↓
         Overmend AI runs local tests
                      ↓
              All tests PASS
                      ↓
   Overmend AI creates a GitHub Pull Request with fix
```
