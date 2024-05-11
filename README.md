# Loans API Documentation

## Overview

This documentation outlines how to set up and use the Loans API, a Django backend designed for secure and efficient management of customer and loan data.

## API Endpoints

The API is structured around the following endpoints:

### Authentication

- **Obtain Token Pair**: `POST /api/token-auth/` - Obtain an access token pair.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Django REST framework

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/Sergioarg/users_api.git
    ```
2. Navigate to the project directory:
   ```
   cd users_api/
   ```
3. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
      ```
      .\venv\Scripts\activate
      ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
5. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```
6. Apply migrations to set up the database:
   ```
   python3 manage.py migrate
   ```
7. Create an admin user:
   ```
    python3 manage.py createsuperuser --username admin --email admin@example.com
   ```

## Running the Server

To start the server, run:
```
python manage.py runserver
```
The server will start at `http://localhost:8000`.

## API Endpoints

- customers:  `http://127.0.0.1:8000/api/customers/`
- loans:  `http://127.0.0.1:8000/api/loans/`
- payments:  `http://127.0.0.1:8000/api/payments/`


### Usage

To interact with the API, you can use tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

- **Obtain API Token**
  - **Endpoint**: `/api/token-auth/`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "username": "exampleuser",
      "password": "examplepassword"
    }
    ```
  - **Response**:
    ```json
    {
      "token": "API-TOKEN"
    }
    ```

### Customers Management

- **Create a Customer**
  - **Endpoint**: `/api/customers/`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "score": 6000,
      "external_id": "customer_01"
    }
    ```
  - **Response**:
    ```json
    {
      "score": "6000.00",
      "status": 1,
      "external_id": "customer_01",
      "preapproved_at": null
    }
    ```

### Loan Management

- **Create a Loan**
  - **Endpoint**: `/api/loans/`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "amount": 4000,
      "external_id": "loan_01",
      "customer": 1
    }
    ```
  - **Response**:
    ```json
    {
      "external_id": "loan_01",
      "amount": "2000.00",
      "status": 1,
      "outstanding": "2000.00",
      "customer_external_id": "customer_01"
    }
    ```
### Payment Management

- **Create a Payment**
  - **Endpoint**: `/api/payments/`
  - **Method**: `POST`
  - **Body**:
    ```json
      {
        "total_amount": 1500,
        "external_id": "payment_02",
        "customer": 1,
        "payment_loan_detail": [
            {"loan": 1, "amount": 1500},
        ]
      }
    ```
  - **Response**:
    ```json
    {
      "total_amount": "1500",
      "status": 4,
      "paid_at": "2024-05-11T23:34:29.703632Z",
      "external_id": "payment_48",
      "customer_external_id": "customer_02",
      "loan_external_id": "loan_02",
      "payment_amount": 1500.0
    }
    ```

### Run Tests
Execute the Django test runner to run all tests in the project.

```bash
python manage.py test
```

## Testing

To run tests, use:
```
python manage.py test
```
