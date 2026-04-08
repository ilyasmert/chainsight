# chAInSight – Backend and Frontend

**chAInSight** is a web-based inventory management system designed to streamline the transfer and tracking of product data across various stages (Ready, In Transit, To Be Produced, Sales, etc.). It features an interactive dashboard, Excel upload capabilities, and predictive analytics potential.  

This repository includes the **Django backend** and **React frontend**, built to work seamlessly together.

---

## 🧩 Tech Stack

- **Backend:** Django + Django REST Framework
- **Frontend:** React + Tailwind CSS
- **Database:** PostgreSQL
- **API Testing:** Postman
- **Excel Parsing:** pandas

---

## 🚀 Features

- View and manage inventory tables (`ready`, `atp_stock`, `intransit`, `sales`, `to_be_produced`)
- Upload Excel files for weekly inventory updates
- Archives historical data automatically upon upload
- Toggle views with React UI (Ready Table, Upload Section, etc.)
- Bulk upload up to 5 Excel files at once
- Update variables in the `transportation_info` table and `pallet_info` page

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
    git clone https://github.com/ilyasmert/chainsight.git
    cd cfecs
```

### 2. Backend Setup 
```bash
    cd chainsight_backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```

#### Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Start server
```bash
python manage.py runserver
```

### 3. Frontend Setup
```bash
    cd chainsight_frontend
    npm install
    npm start
```

## 🔗 API Endpoints

All API endpoints are prefixed with:
    http://127.0.0.1:8000/api/inventory/

### 1. Inventory Endpoints
| Method | Endpoint                   | Description                                                                    |
|--------|----------------------------|--------------------------------------------------------------------------------|
| GET    | `/ready/`                  | Retrieve all items in the `ready` table                                        |
| GET    | `/atp_stock/`              | Retrieve all items in the `atp_stock` table                                    |
| GET    | `/intransit/`              | Retrieve all items in the `intransit` table                                    |
| GET    | `/sales/`                  | Retrieve all items in the `sales` table                                        |
| GET    | `/to_be_produced/`         | Retrieve all items in the `to_be_produced` table                               |
| POST   | `/ready/`                  | Add a new item to the `ready` table                                            |
| POST   | `/atp_stock/`              | Add a new item to the `atp_stock` table                                        |
| POST   | `/intransit/`              | Add a new item to the `intransit` table                                        |
| POST   | `/sales/`                  | Add a new item to the `sales` table                                            |
| POST   | `/to_be_produced/`         | Add a new item to the `to_be_produced` table                                   |
| PUT    | `/ready/<id>/`             | Update an item in the `ready` table                                            |
| PUT    | `/atp_stock/<id>/`         | Update an item in the `atp_stock` table                                        |
| PUT    | `/intransit/<id>/`         | Update an item in the `intransit` table                                        |
| PUT    | `/sales/<id>/`             | Update an item in the `sales` table                                            |
| PUT    | `/to_be_produced/<id>/`    | Update an item in the `to_be_produced` table                                   |
| DELETE | `/ready/<id>/`             | Delete an item from the `ready` table                                          |
| DELETE | `/atp_stock/<id>/`         | Delete an item from the `atp_stock` table                                      |
| DELETE | `/intransit/<id>/`         | Delete an item from the `intransit` table                                      |
| DELETE | `/sales/<id>/`             | Delete an item from the `sales` table                                          |
| DELETE | `/to_be_produced/<id>/`    | Delete an item from the `to_be_produced` table                                 |
| GET    | `/transportation/`         | Retrieve a specific transportation record from `transportation_info` table     |
| POST   | `/transportation/archive/` | Archive current data in `transportation_info` to `transportation_info_archive` |
| PUT    | `/transportation/update/`  | Update `transportation_info` with parameters given by the user                 |

### 2. Excel Upload Endpoint
| Method | Endpoint         | Description                          |
|--------|------------------|--------------------------------------|
| POST   | `/upload-table/` | Upload an Excel file for inventory update |

Parameters:
- `file`: The Excel file to be uploaded (must be in `.xlsx` format).
- `tableName`: The table to which the data should be uploaded (e.g., `ready`, `atp_stock`, etc.).
- `archivedBy`: User who uploads the files. (default: `admin`).

Sample CURL request:
```bash
curl -X POST http://127.0.0.1:8000/api/inventory/upload-table/ \
  -F "tableName=ready" \
  -F "archivedBy=admin" \
  -F "file=@ready.xlsx"
```

## 📬 Using Postman

A ready-to-use Postman Collection is included in the repo:

    postman/InventoryAPI.postman_collection.json

Import this into Postman to test all endpoints easily.# chainsight
