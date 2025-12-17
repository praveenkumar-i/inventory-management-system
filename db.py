import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="inventory_Database"
    )
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Products Table 
        # Stores Product ID and Name
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL UNIQUE
            )
        """)

        # 2. Locations Table 
        # Stores Warehouse/Location Names
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                location_id INT AUTO_INCREMENT PRIMARY KEY,
                location_name VARCHAR(255) NOT NULL UNIQUE
            )
        """)

        # 3. Product Movements Table 
        # Tracks movement of products between locations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_movements (
                movement_id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                from_location INT,
                to_location INT,
                product_id INT,
                qty INT,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (from_location) REFERENCES locations(location_id),
                FOREIGN KEY (to_location) REFERENCES locations(location_id)
            )
        """)
        
        conn.commit()
        print("✅ Success! Database Tables Created Successfully.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    init_db()


# --- PRODUCTS MANAGEMENT FUNCTIONS ---

# 1. Add New Product
def add_product(product_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # insert new product name
        cursor.execute("INSERT INTO products (product_name) VALUES (%s)", (product_name,))
        conn.commit()
        print(f"✅ Product '{product_name}' Added!")
    except mysql.connector.IntegrityError:
        print(f"❌ Error: Product '{product_name}' already exists!")
    finally:
        cursor.close()
        conn.close()

# 2. Get All Products (View)
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# 3. Get Single Product by ID (need for before edit)
def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product

# 4. Update Product
def update_product(product_id, new_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET product_name = %s WHERE product_id = %s", (new_name, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Product Updated!")


# --- LOCATIONS MANAGEMENT FUNCTIONS ---

# 1. Add New Location
def add_location(location_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO locations (location_name) VALUES (%s)", (location_name,))
        conn.commit()
        print(f"✅ Location '{location_name}' Added!")
    except mysql.connector.IntegrityError:
        print(f"❌ Error: Location '{location_name}' already exists!")
    finally:
        cursor.close()
        conn.close()

# 2. Get All Locations
def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    cursor.close()
    conn.close()
    return locations

# 3. Get Single Location by ID
def get_location_by_id(location_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM locations WHERE location_id = %s", (location_id,))
    location = cursor.fetchone()
    cursor.close()
    conn.close()
    return location

# 4. Update Location
def update_location(location_id, new_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE locations SET location_name = %s WHERE location_id = %s", (new_name, location_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Location Updated!")


# --- PRODUCT MOVEMENT FUNCTIONS ---

# 1. Add Movement (Main Logic)
def add_movement(product_id, qty, from_loc, to_loc):
    conn = get_db_connection()
    cursor = conn.cursor()
    
   # If 'None' is selected in the dropdown, it should be stored as NULL in the database."
    if from_loc == "": from_loc = None
    if to_loc == "": to_loc = None

    # Insert into movement table
    query = """
        INSERT INTO product_movements (product_id, qty, from_location, to_location) 
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (product_id, qty, from_loc, to_loc))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Movement Recorded!")

# 2. Get All Movements (History View with Names)
def get_movements():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # # JOIN query: To retrieve the Name based on the ID
    query = """
        SELECT 
            m.movement_id, 
            m.timestamp, 
            m.qty, 
            p.product_name, 
            lf.location_name as from_loc, 
            lt.location_name as to_loc
        FROM product_movements m
        JOIN products p ON m.product_id = p.product_id
        LEFT JOIN locations lf ON m.from_location = lf.location_id
        LEFT JOIN locations lt ON m.to_location = lt.location_id
        ORDER BY m.timestamp DESC
    """
    
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    conn.close()
    return movements


# --- REPORT FUNCTION (Final Requirement) ---

def get_balance_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Advanced SQL Query to calculate Inventory Balance:
    # 1. CROSS JOIN: Create all possible Product-Location combinations.
    # 2. Add (+): Sum quantities where product moved TO a location.
    # 3. Subtract (-): Deduct quantities where product moved FROM a location.
    # 4. Filter: Show only locations with Positive Balance (> 0).
    
    query = """
        SELECT 
            p.product_name,
            l.location_name,
            SUM(CASE 
                WHEN m.to_location = l.location_id THEN m.qty 
                WHEN m.from_location = l.location_id THEN -m.qty 
                ELSE 0 
            END) as qty
        FROM locations l
        CROSS JOIN products p
        LEFT JOIN product_movements m 
            ON m.product_id = p.product_id 
            AND (m.to_location = l.location_id OR m.from_location = l.location_id)
        GROUP BY p.product_id, l.location_id
        HAVING qty > 0
        ORDER BY l.location_name, p.product_name;
    """
    
    cursor.execute(query)
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return report

# --- STOCK CHECK FUNCTION ---
def get_stock_at_location(product_id, location_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Retrieve movement history for this specific product
    cursor.execute("SELECT * FROM product_movements WHERE product_id = %s", (product_id,))
    movements = cursor.fetchall()
    conn.close()
    
    balance = 0
    for mov in movements:
        # If stock moved IN, add to balance (+)
        if mov['to_location'] == location_id:
            balance += mov['qty']
        # If stock moved OUT, deduct from balance (-)
        if mov['from_location'] == location_id:
            balance -= mov['qty']
            
    return balance
