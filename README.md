# Book Management System

This Book Management System was built using **FastAPI**, **MySQL**, and **Pydantic** for data validation. This file explains how to set up, run the application, perform API testing using Postman, and execute necessary SQL queries.

---

## Prerequisites

1. **Python**: Install Python 3.10 or later.
2. **MySQL**: Install MySQL server and ensure it is running.
3. **pip**: Ensure you have `pip` installed to manage Python packages.
4. **Postman**: Install Postman for API testing.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/BiploveGC/book_management_system.git
cd book_management_system
```

### 2. Install Dependencies

Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows
pip install fastapi uvicorn sqlalchemy mysqlclient pydantic
```

### 3. Configure Database

Update the `DATABASE_URL` in the source code with your MySQL database credentials:

```python
DATABASE_URL = "mysql://<username>:<password>@<host>/<database_name>"
```

#### Example:

```python
DATABASE_URL = "mysql://root:MySecurePassword@localhost/book_management"
```

Create the database if it doesn’t already exist:

```sql
CREATE DATABASE book_management;
```

### 4. Run the Application

Run the FastAPI application using the `uvicorn` server:

```bash
uvicorn main:app --reload
```

- The app will be accessible at: `http://127.0.0.1:8000`
- Open the **API documentation** in your browser: `http://127.0.0.1:8000/docs`

---

## API Testing with Postman

### 1. Create a New Collection

- Open Postman and create a new collection named `Book Management`.
- Add requests for each endpoint.

### 2. Endpoints and Sample Requests

#### **1. Create a New Book**

**Endpoint:**

```http
POST /books
```

**Body (JSON):**

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "description": "A novel set in the Roaring Twenties.",
  "isbn": "1234567890123",
  "published_year": 1925
}
```

#### **2. Get All Books**

**Endpoint:**

```http
GET /books
```

#### **3. Get a Book by ID**

**Endpoint:**

```http
GET /books/{book_id}
```

Replace `{book_id}` with the ID of the book you want to retrieve (e.g., `/books/1`).

#### **4. Update a Book**

**Endpoint:**

```http
PUT /books/{book_id}
```

**Body (JSON):**

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "description": "An updated description.",
  "isbn": "1234567890123",
  "published_year": 1925
}
```

#### **5. Delete a Book**

**Endpoint:**

```http
DELETE /books/{book_id}
```

Replace `{book_id}` with the ID of the book you want to delete (e.g., `/books/1`).

---

## SQL Queries

### 1. Create Database

```sql
CREATE DATABASE book_management;
```

`

### 2. View All Books

To view all books in the database:

```sql
SELECT * FROM books;
```

### 3. Add a Book Manually

Insert a new book into the `books` table:

```sql
INSERT INTO books (title, author, description, isbn, published_year)
VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 'A novel set in the Roaring Twenties.', '1234567890123', 1925);
```

### 4. Update a Book Record

```sql
UPDATE books
SET description = 'An updated description.'
WHERE id = 1;
```

### 5. Delete a Book Record

```sql
DELETE FROM books
WHERE id = 1;
```

### 6. Search for a Book by Title

```sql
SELECT * FROM books
WHERE title LIKE '%Gatsby%';
```

---

## Troubleshooting

### Common Issues

1. **Database Connection Error**:

   - Ensure the MySQL server is running.
   - Verify that `DATABASE_URL` is correctly configured.

2. **Table Not Found**:

   - Ensure the database tables are initialized by running the app (`python main.py`).

3. **Package installation**:

   - Run `pip install pip install fastapi uvicorn sqlalchemy mysqlclient pydantic ` to install all packages.

---


---

## Additional Resources

- **FastAPI Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **SQLAlchemy Documentation**: [https://docs.sqlalchemy.org](https://docs.sqlalchemy.org)
- **Postman**: [https://www.postman.com](https://www.postman.com)

---

This guide provides step-by-step instructions for setting up, running, and testing the Book Management System. Happy coding!


