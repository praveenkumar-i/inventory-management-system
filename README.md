# Inventory Management Web Application 📦

A web-based Inventory Management application built using **Python (Flask)** and **MySQL**. This system helps in tracking products, managing stock levels, and handling product movements efficiently.

## 🚀 Key Features

1. **Product Management:**
   * Add and Edit Products.
   * Clean and user-friendly interface.

2. **Location Management:**
   * Add and Edit warehouse/locations.

3. **Smart Stock Movements:**
   * Move products between locations (Purchases/Sales).
   * Maintains a complete log of all transfers with **Time, Date, Product, Qty, From Location and To Location details**.
   
   **Stock Validation:**
     If stock is not available in the source location, it shows an error (Server-side validation included).

4. **Real-Time Reporting:**
   * View live inventory balances across all locations.
   
   **Search & Filter:**
      Includes a dynamic search bar to quickly find products or locations in the report.

    **Database:**
      Used Raw SQL queries (MySQL).

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript

## ⚙️ Setup & Installation Instructions



Follow these steps to run the project locally:



1.  **Clone the Repository**

    ```bash

    git clone [https://github.com/praveenkumar-i/inventory-management-system.git](https://github.com/praveenkumar-i/inventory-management-system.git)

    cd inventory-management-system

    ```



2.  **Install Dependencies**

    ```bash

    pip install -r requirements.txt

    ```



3.  **Database Configuration**

    * Ensure **XAMPP (MySQL)** is running.

    * Open `db.py` and update your MySQL credentials (`db_config`) if necessary.

    * Run the setup script to create tables:

        ```bash

        python db.py

        ```



4.  **Run the Application**

    ```bash

    python app.py

    ```

    * Open your browser and visit: `http://127.0.0.1:5000`



## 📸 Screenshots

*(Please check the `project_screenshots` folder in this repository to view the Project Dashboard, Movements, and Reports)*



---

*Submitted by: PraveenKumar I*

