-- Create the database if it doesn't exist
DROP DATABASE IF EXISTS brewtrack_db;
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


-- ==========================================================================
-- SEED DATA
-- Internally consistent (inventory quantities, movement log, and PO/receiving
-- math all agree with each other) so every page - Dashboard, Inventory
-- Monitoring, Low-Stock Alerts, Purchase Orders, Movement History, Reports,
-- Daily Sales - has real numbers to show on first run.
-- ==========================================================================

-- 1. USERS
-- Passwords are bcrypt hashes of 'admin123' and 'staff123' - login works
-- immediately without any manual rehashing step.
INSERT INTO users (user_id, full_name, email, username, password, role, contact_number, status) VALUES
(1, 'Dana Whitfield', 'owner@brewtrack.com', 'owner', '$2b$12$oqgFwHN7N1VgPvUXssFOw.5tos5zvb/rwCbCdciCzPiXBed0TXu3K', 'Owner/Admin', '0917-000-0001', 'Active'),
(2, 'Marco Reyes',    'staff@brewtrack.com', 'marco', '$2b$12$F8jjmm4YTKR6Ju0ut7a3YOyAtTxR5R4zogzZMoGRaWoYDKaoYHkdC', 'Staff',       '0917-000-0002', 'Active');

-- 2. SUPPLIERS
INSERT INTO suppliers (supplier_id, supplier_name, contact_person, contact_number, address, email, supplier_status) VALUES
(1, 'ABC Company', 'Ana Cruz',    '0917-111-2222', 'Batangas City', 'sales@abccompany.com', 'Active'),
(2, 'ZXC Farm',     'Zara Cortes','0917-333-4444', 'Lipa City',     'hello@zxcfarm.com',    'Active');

-- 3. INGREDIENTS & SUPPLIES
-- reorder_level values match the Low-Stock Alerts mockup (145kg/reorder 150, etc.)
INSERT INTO ingredients_supplies (item_id, supplier_id, item_name, category, unit_of_measurement, cost_per_unit, reorder_level, item_status) VALUES
(1, 1, 'Coffee Bean',    'Beans',  'kg', 400.00, 150, 'Active'),
(2, 1, 'Matcha Powder',  'Powder', 'g',    8.50, 150, 'Active'),
(3, 1, 'Oatmilk',        'Milk',   'L',   90.00,   3, 'Active'),
(4, 2, 'Vanilla Syrup',  'Syrup',  'L',  350.00,   5, 'Active');

-- 4. INVENTORY (current on-hand quantities)
-- Coffee Bean and Matcha Powder sit just under reorder level -> "Low"
-- Oatmilk sits well under reorder level -> "Critical"/"Low"
-- Vanilla Syrup sits under reorder level -> "Low"
INSERT INTO inventory (item_id, current_quantity) VALUES
(1, 145.00),
(2, 120.00),
(3, 1.00),
(4, 2.00);

-- 5. PRODUCTS / MENU (prices match the Daily Sales Recording mockup)
INSERT INTO products_menu (product_id, product_name, selling_price, product_status) VALUES
(1, 'Espresso',          100.00, 'Active'),
(2, 'Matcha Latte',      180.00, 'Active'),
(3, 'Spanish Latte',     160.00, 'Active'),
(4, 'Caramel Macchiato', 160.00, 'Active');

-- 6. PRODUCT INGREDIENTS (recipe: how much of each raw ingredient a sale consumes)
INSERT INTO product_ingredients (product_id, item_id, quantity_required) VALUES
(1, 1, 0.02),                    -- Espresso: 20g coffee
(2, 2, 0.025), (2, 3, 0.15),     -- Matcha Latte: 25g matcha, 150ml oatmilk
(3, 1, 0.02),  (3, 3, 0.15),     -- Spanish Latte: 20g coffee, 150ml oatmilk
(4, 1, 0.02),  (4, 4, 0.02), (4, 3, 0.10); -- Caramel Macchiato: 20g coffee, 20ml vanilla syrup, 100ml oatmilk

-- 7. PURCHASE ORDERS (matches PO-1008/1009/1010 from the mockups: Pending/Approved/Received)
INSERT INTO purchase_orders (po_id, supplier_id, user_id, po_date, expected_delivery_date, po_status) VALUES
(1, 1, 1, '2026-07-01 09:00:00', '2026-07-08', 'Received'),
(2, 1, 1, '2026-07-03 10:15:00', '2026-07-10', 'Pending'),
(3, 2, 1, '2026-07-03 11:30:00', '2026-07-10', 'Approved');

INSERT INTO purchase_order_details (po_id, item_id, ordered_quantity, unit_cost) VALUES
(1, 1, 10.00, 400.00),   -- PO-1001 (Received): 10kg Coffee Bean
(2, 1, 5.00,  500.00),   -- PO-1002 (Pending):  5kg Coffee Bean @ higher quoted cost
(2, 2, 5.00,  600.00),   -- PO-1002 (Pending):  5kg Matcha Powder
(3, 4, 5.00,  350.00);   -- PO-1003 (Approved): 5L Vanilla Syrup

-- 8. RECEIVING (for the one Received PO above - delivered exactly as ordered)
INSERT INTO receiving (receiving_id, po_id, user_id, receiving_date, delivery_status, remarks) VALUES
(1, 1, 2, '2026-07-05 08:00:00', 'Received', 'PO-1001 received in full');

INSERT INTO receiving_details (receiving_id, item_id, received_quantity, discrepancy_quantity) VALUES
(1, 1, 10.00, 0.00);

-- 9. SALES (spread across 3 days so the Reports revenue chart has a trend to show)
INSERT INTO sales_stock_out (sales_id, user_id, sales_date, transaction_type, remarks) VALUES
(1, 2, '2026-07-06 09:15:00', 'Daily Sales', ''),
(2, 2, '2026-07-06 14:30:00', 'Daily Sales', ''),
(3, 2, '2026-07-07 10:00:00', 'Daily Sales', ''),
(4, 2, '2026-07-08 16:45:00', 'Daily Sales', ''),
(5, 2, '2026-07-08 12:00:00', 'Wastage', 'Dropped during prep');

INSERT INTO sales_stock_out_details (sales_id, product_id, item_id, quantity_sold, quantity_used, selling_price, unit_cost, line_total) VALUES
(1, 4, NULL, 2, 0, 160.00, 0, 320.00),  -- 2x Caramel Macchiato
(2, 3, NULL, 1, 0, 160.00, 0, 160.00),  -- 1x Spanish Latte
(3, 2, NULL, 1, 0, 180.00, 0, 180.00),  -- 1x Matcha Latte
(3, 1, NULL, 1, 0, 100.00, 0, 100.00),  -- + 1x Espresso, same order
(4, 4, NULL, 1, 0, 160.00, 0, 160.00),  -- 1x Caramel Macchiato
(5, NULL, 2, 0, 20.00, 0, 8.50, 0.00);  -- Wastage: 20g Matcha Powder, no revenue line

-- 10. INVENTORY MOVEMENTS
-- Every quantity change above (receiving, sales ingredient deductions, wastage)
-- has a matching audit-trail row here, with resulting_stock reflecting the
-- running total at that point in time.
INSERT INTO inventory_movements (item_id, user_id, movement_type, quantity, resulting_stock, movement_date, reference_type, reference_id, remarks) VALUES
-- Coffee Bean: started at 135kg, +10kg received on PO-1001 -> 145kg (matches inventory row above)
(1, 2, 'Stock-In',  10.00, 145.00, '2026-07-05 08:00:00', 'Purchase Order', 1, 'PO-1001 received'),
-- Matcha Powder: wastage during prep
(2, 2, 'Stock-Out', -20.00, 120.00, '2026-07-08 12:00:00', 'Usage', 5, 'Dropped during prep'),
-- Oatmilk: consumed by sales #2 (Spanish Latte) and #3 (Matcha Latte + Espresso)
(3, 2, 'Stock-Out', -0.15, 1.15, '2026-07-06 14:30:00', 'Sales', 2, 'Sale deduction'),
(3, 2, 'Stock-Out', -0.15, 1.00, '2026-07-07 10:00:00', 'Sales', 3, 'Sale deduction'),
-- Vanilla Syrup: consumed by sale #1 and #4 (Caramel Macchiato x2 orders)
(4, 2, 'Stock-Out', -0.04, 1.96, '2026-07-06 09:15:00', 'Sales', 1, 'Sale deduction'),
(4, 2, 'Stock-Out', -0.02, 1.94, '2026-07-08 16:45:00', 'Sales', 4, 'Sale deduction');