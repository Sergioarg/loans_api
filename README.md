<!-- # Project Documentation: Users API

## Overview

The Users API is a Django-based RESTful API designed to manage user data and provide authentication using JSON Web Tokens (JWT). This project aims to offer a robust backend solution for user data management, including CRUD operations and secure user authentication.

## Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST framework**: An extension for Django that provides tools for building Web APIs.
- **Django REST framework Simple JWT**: A library for adding JWT authentication to Django REST framework.

## Project Structure

The project is organized into a Django project directory (`api`) and an application directory (`users_data`) within it. The `users_data` app contains models, serializers, views, and other files related to user data management.

## API Endpoints

The API is structured around the following endpoints:

### User Management

- **List Users**: `GET /users/` - Retrieve a list of all users. **(Need TOKEN)**
- **Create User**: `POST /users/` - Create a new user.
- **Retrieve User**: `GET /users/{id}/` - Retrieve a specific user by ID. **(Need TOKEN)**
- **Update User**: `PUT /users/{id}/` - Update a specific user by ID. **(Need TOKEN)**
- **Delete User**: `DELETE /users/{id}/` - Delete a specific user by ID. **(Need TOKEN)**

### Authentication

- **Obtain Token Pair**: `POST /api/token/` - Obtain an access and refresh token pair.
- **Refresh Token**: `POST /api/token/refresh/` - Refresh an access token using a refresh token.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Django REST framework
- Django REST framework Simple JWT

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Sergioarg/users_api.git
   ```
2. Navigate to the project directory:
   ```
   cd users_api/
   ```
3. Install the required dependencies:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python3 manage.py migrate
   ```
5. Crate admin user:
   ```
   python3 manage.py createsuperuser --username admin --email admin@example.com
   ```
6. Run the server:
   ```
   python3 manage.py runserver
   ```

### Usage

To interact with the API, you can use tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

#### Example: Create a New User

```bash
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{"username": "newuser", "email": "example@gmail.com", "password": "newpassword"}'
```
#### Example: Get User

```bash
curl -X GET http://localhost:8000/users/ -H "Content-Type: application/json Authorization: Bearer YOUR TOKEN" -d '{"username": "newuser", "email": "example@gmail.com", "password": "newpassword"}'
```

#### Example: Obtain JWT Tokens

```bash
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "newuser", "password": "newpassword"}'
```

### Run Tests
Execute the Django test runner to run all tests in the project.

```bash
python manage.py test
```
### Example Test Output

```
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 2.935s

OK
Destroying test database for alias 'default'...
``` -->
Customer:
    GET: /customer
    BALANCE GET: /customer/{external_id}/balance/
    Loans GET: /customer/{external_id}/loans/

Loans:
    GET: 


Payments:
    GET: /payments/{external_id}

    "results": [
`curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token <ADD_TOKEN>'`
