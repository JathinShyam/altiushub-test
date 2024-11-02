# Invoice Management API

## Description

A Django REST Framework based API for managing invoices with support for invoice items and bill sundries. This API provides complete CRUD operations for invoices while maintaining data integrity and automated calculations.

## Features

- Full CRUD operations for invoices
- Auto-incrementing invoice numbers
- Automated calculations for:
  - Invoice item amounts (quantity × price)
  - Total invoice amount (sum of items + sundries)
- Data validation for:
  - Positive prices and quantities
  - Proper amount calculations
  - Unique invoice numbers
- Support for bill sundries with positive/negative amounts
- Nested operations for invoice items and bill sundries

## Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default) / PostgreSQL (recommended for production)

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:JathinShyam/altiushub-test.git
   cd altiushub-test
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Endpoints

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| GET    | `/invoices/`        | List all invoices         |
| POST   | `/invoices/`        | Create a new invoice      |
| GET    | `/invoices/{uuid}/` | Retrieve specific invoice |
| PUT    | `/invoices/{uuid}/` | Update specific invoice   |
| PATCH  | `/invoices/{uuid}/` | Partially update invoice  |
| DELETE | `/invoices/{uuid}/` | Delete specific invoice   |

### Example Requests

#### Create Invoice

```json
POST /api/invoices/

{
    "date": "2024-11-02T10:00:00Z",
    "customer_name": "John Doe",
    "billing_address": "123 Billing St",
    "shipping_address": "456 Shipping Ave",
    "gstin": "GSTIN123456",
    "invoice_items": [
        {
            "item_name": "Product 1",
            "quantity": 2,
            "price": 100.00
        }
    ],
    "bill_sundries": [
        {
            "bill_sundry_name": "Shipping",
            "amount": 50.00
        }
    ]
}
```

#### Update Invoice

```json
PUT /api/invoices/{uuid}/

{
    "date": "2024-11-02T10:00:00Z",
    "customer_name": "John Doe Updated",
    "billing_address": "123 New Billing St",
    "shipping_address": "456 New Shipping Ave",
    "gstin": "GSTIN123456",
    "invoice_items": [
        {
            "item_name": "Updated Product",
            "quantity": 3,
            "price": 150.00
        }
    ],
    "bill_sundries": [
        {
            "bill_sundry_name": "Express Shipping",
            "amount": 75.00
        }
    ]
}
```

## Models

### Invoice

- `id`: UUID (Primary Key)
- `date`: DateTime (UTC)
- `invoice_number`: AutoIncrement
- `customer_name`: String
- `billing_address`: Text
- `shipping_address`: Text
- `gstin`: String
- `total_amount`: Decimal

### Invoice Item

- `id`: UUID (Primary Key)
- `invoice`: ForeignKey to Invoice
- `item_name`: String
- `quantity`: Decimal (> 0)
- `price`: Decimal (> 0)
- `amount`: Decimal (calculated)

### Invoice Bill Sundry

- `id`: UUID (Primary Key)
- `invoice`: ForeignKey to Invoice
- `bill_sundry_name`: String
- `amount`: Decimal (can be positive or negative)

## Validation Rules

### 1. Invoice Items

- Amount = Quantity × Price
- Price and Quantity must be greater than zero
- Amount is automatically calculated

### 2. Bill Sundries

- Amount can be positive or negative

### 3. Invoice

- Total Amount = Sum(Invoice Items Amount) + Sum(Bill Sundries Amount)
- Invoice Number is auto-incremental and unique

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Successful operation
- 201: Successfully created
- 400: Bad request (validation errors)
- 404: Resource not found
- 500: Server error
