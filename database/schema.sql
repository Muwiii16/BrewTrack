-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS brewtrack_db;
USE brewtrack_db;

-- ==========================================
-- 1. USER TABLE
-- ==========================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Length accommodates hashed passwords (e.g., bcrypt)
    role VARCHAR(30) NOT NULL,
    contact_number VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Active'
);

-- ==========================================
-- 2. SUPPLIER TABLE
-- ==========================================
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    contact_number VARCHAR(20),
    address TEXT,
    email VARCHAR(100),
    supplier_status VARCHAR(20) DEFAULT 'Active'
);

-- ==========================================
-- 3. INGREDIENT/SUPPLY TABLE
-- ==========================================
CREATE TABLE ingredients_supplies (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_of_measurement VARCHAR(20) NOT NULL, -- e.g., kg, liters, pcs
    cost_per_unit DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    reorder_level INT NOT NULL DEFAULT 0,
    item_status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE SET NULL
);

-- ==========================================
-- 4. INVENTORY TABLE
-- ==========================================
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT UNIQUE, -- Unique enforces the 1:1 relationship with ingredients_supplies
    current_quantity DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE CASCADE
);

-- ==========================================
-- 5. PRODUCT / MENU ITEM TABLE
-- ==========================================
CREATE TABLE products_menu (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    selling_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    product_status VARCHAR(20) DEFAULT 'Active'
);

-- ==========================================
-- 6. PRODUCT INGREDIENT (Bridge Table)
-- ==========================================
CREATE TABLE product_ingredients (
    product_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_required DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_menu(product_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE RESTRICT
);

-- ==========================================
-- 7. PURCHASE ORDER TABLE
-- ==========================================
CREATE TABLE purchase_orders (
    po_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    user_id INT NOT NULL,
    po_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_delivery_date DATE,
    po_status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ==========================================
-- 8. PURCHASE ORDER DETAIL TABLE
-- ==========================================
CREATE TABLE purchase_order_details (
    po_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    po_id INT NOT NULL,
    item_id INT NOT NULL,
    ordered_quantity DECIMAL(10, 2) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) GENERATED ALWAYS AS (ordered_quantity * unit_cost) STORED, -- Auto-calculated column
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE RESTRICT
);

-- ==========================================
-- 9. RECEIVING TABLE
-- ==========================================
CREATE TABLE receiving (
    receiving_id INT AUTO_INCREMENT PRIMARY KEY,
    po_id INT NOT NULL,
    user_id INT NOT NULL,
    receiving_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_status VARCHAR(30) DEFAULT 'Received',
    remarks TEXT,
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ==========================================
-- 10. RECEIVING DETAIL TABLE
-- ==========================================
CREATE TABLE receiving_details (
    receiving_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    receiving_id INT NOT NULL,
    item_id INT NOT NULL,
    received_quantity DECIMAL(10, 2) NOT NULL,
    discrepancy_quantity DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (receiving_id) REFERENCES receiving(receiving_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE RESTRICT
);

-- ==========================================
-- 11. STOCK-OUT/SALES TABLE
-- ==========================================
CREATE TABLE sales_stock_out (
    sales_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    sales_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    transaction_type VARCHAR(30) NOT NULL, -- e.g., 'Daily Sales', 'Wastage', 'Manual Adjustment'
    remarks TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ==========================================
-- 12. STOCK-OUT/SALES DETAIL TABLE
-- ==========================================
CREATE TABLE sales_stock_out_details (
    sales_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    sales_id INT NOT NULL,
    product_id INT NULL, -- Nullable because manual stock-outs might just log the raw item
    item_id INT NULL,    -- Nullable because typical menu sales point directly to product_id
    quantity_sold INT DEFAULT 0,
    quantity_used DECIMAL(10, 2) DEFAULT 0.00,
    selling_price DECIMAL(10, 2) DEFAULT 0.00,
    unit_cost DECIMAL(10, 2) DEFAULT 0.00,
    line_total DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Handled programmatically based on logic
    FOREIGN KEY (sales_id) REFERENCES sales_stock_out(sales_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_menu(product_id) ON DELETE SET NULL,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE SET NULL
);

-- ==========================================
-- 13. INVENTORY MOVEMENT TABLE
-- ==========================================
CREATE TABLE inventory_movements (
    movement_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    user_id INT NOT NULL,
    movement_type VARCHAR(30) NOT NULL, -- e.g., 'Stock-In', 'Stock-Out', 'Adjustment'
    quantity DECIMAL(10, 2) NOT NULL,
    resulting_stock DECIMAL(10, 2) NOT NULL,
    movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    reference_type VARCHAR(50),         -- e.g., 'Purchase Order', 'Sales'
    reference_id INT,                   -- Stores corresponding po_id, sales_id, etc.
    remarks TEXT,
    FOREIGN KEY (item_id) REFERENCES ingredients_supplies(item_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ==========================================
-- PERFORMANCE INDEXES (Highly Recommended)
-- ==========================================
CREATE INDEX idx_item_category ON ingredients_supplies(category);
CREATE INDEX idx_po_status ON purchase_orders(po_status);
CREATE INDEX idx_movement_date ON inventory_movements(movement_date);
CREATE INDEX idx_sales_date ON sales_stock_out(sales_date);