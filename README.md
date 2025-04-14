# **Home Budget API**

A backend application for managing personal finances. It provides RESTful endpoints for user authentication, category and expense management, and data aggregation.

---

## **Getting Started**

### **Run the Project**

1. Clone the repository:  
   `git clone https://github.com/Tunjo/devot-home-budget-api.git`  
   `cd devot-home-budget-api`

2. Start the project:  
   `make run-dev`  
   This command will:

   - Build the Docker containers for the backend and database.
   - Apply database migrations.
   - Create a superuser
   - Add predefined categories like `Food & Groceries`, `Transportation`, and `Rent & Utilities`.
   - Start the development server at `http://127.0.0.1:8000`.

   Once the server is running:

   - API documentation: `http://127.0.0.1:8000/docs/`
   - redoc: `http://127.0.0.1:8000/redoc/`.
   - download schema: `http://127.0.0.1:8000/schema/`
   - admin panel: `http://127.0.0.1:8000/admin/`
     - **Username**: `devotadmin`
     - **Password**: `devot!admin`

---

### **Load Test Data**

Run the following command to quickly set up additional data for the application:  
`make run-data`

This command will:

- Create a test user for you to log in and test the application.
- Add an additional category and some sample expenses, so you don’t have to manually create data via the API.

- **Test User**:
  - **Username**: `devotuser`
  - **Password**: `devot!user`

This step is optional but useful for quickly testing the application without manually adding data.

---

### **Run Tests**

Run the test suite:  
`make backend-tests`

This command will:

- Clean up any stale `__pycache__` and `.pyc` files.
- Run all tests inside the Docker container using `pytest`.

---

### **Summary**

- Use `make run-dev` to start the project, create a superuser, and load predefined categories.
- Use `make run-data` to add additional test data, including a test user and sample expenses.
- Use `make backend-tests` to run the test suite and verify the application.
