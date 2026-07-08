import sys
import os

# Ensure the project root is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_model import add_user, get_users
from models.supplier_model import add_supplier, get_suppliers
from models.ingredient_model import add_ingredient
from models.inventory_model import stock_in
from models.purchase_order_model import create_purchase_order

def seed_database():
    print("=== BrewTrack Realistic Database Seeder ===")
    
    try:
        # --- 1. ADMIN USER ---
        existing_users = get_users()
        admin = next((u for u in existing_users if u['email'] == 'admin@brewtrack.com'), None)
        
        if not admin:
            print("Creating default Admin user...")
            add_user("John Edgar Emmanuel Perez", "admin@brewtrack.com", "admin", "admin_password123", "Owner/ Admin", "09123456789")
            admin = get_users()[-1] # Fetch the newly created user
        
        user_id = admin['user_id']

        # Prevent double-seeding if suppliers already exist
        if len(get_suppliers()) > 0:
            print("⚠️  Database already contains suppliers. Please truncate tables if you want a fresh seed.")
            return

        # --- 2. SUPPLIERS ---
        print("Seeding Suppliers...")
        add_supplier("BFC Roasters Co.", "Juan Roaster", "09123456789", "Makati City", "sales@bfcroasters.com")
        add_supplier("Dairy Best Farms", "Maria Cow", "09876543210", "Batangas", "orders@dairybest.com")
        add_supplier("Sweet Syrups Inc.", "Syrup Sam", "09112223333", "Manila", "hello@sweetsyrups.com")
        add_supplier("EcoPack Solutions", "Pack Patty", "09998887777", "Quezon City", "sales@ecopack.com")

        # Fetch inserted suppliers to map their IDs
        suppliers = {s['supplier_name']: s['supplier_id'] for s in get_suppliers()}

        # --- 3. INGREDIENTS & SUPPLIES ---
        print("Seeding Menu Ingredients & Supplies...")
        ingredients_data = [
            # Supplier ID, Name, Category, UOM, Unit Cost, Reorder Level
            (suppliers["BFC Roasters Co."], "Arabica Espresso Beans", "Coffee", "kg", 650.00, 10.0),
            (suppliers["BFC Roasters Co."], "Vietnamese Coffee Blend", "Coffee", "kg", 550.00, 5.0),
            
            (suppliers["Dairy Best Farms"], "Full Cream Milk", "Dairy", "L", 85.00, 20.0),
            (suppliers["Dairy Best Farms"], "Oat Milk", "Dairy Alternative", "L", 150.00, 10.0),
            
            (suppliers["Sweet Syrups Inc."], "Premium Matcha Powder", "Powder", "kg", 900.00, 3.0),
            (suppliers["Sweet Syrups Inc."], "Vanilla Syrup", "Syrup", "bottle", 320.00, 5.0),
            (suppliers["Sweet Syrups Inc."], "Butterscotch Sauce", "Syrup", "bottle", 350.00, 4.0),
            (suppliers["Sweet Syrups Inc."], "Auro Chocolate Powder", "Powder", "kg", 750.00, 5.0),
            
            (suppliers["EcoPack Solutions"], "16oz Plastic Cups (Iced)", "Packaging", "pcs", 2.50, 300.0),
            (suppliers["EcoPack Solutions"], "500ml Glass Jars", "Packaging", "pcs", 18.00, 100.0),
        ]

        ingredient_ids = {}
        for sup_id, name, cat, uom, cost, ro_level in ingredients_data:
            item_id = add_ingredient(sup_id, name, cat, uom, cost, ro_level)
            ingredient_ids[name] = item_id

        # --- 4. ADJUST INVENTORY (Creating fake stock levels for alerts) ---
        print("Adjusting Inventory Levels (triggering low stock alerts)...")
        stock_levels = {
            "Arabica Espresso Beans": 15.0,     # Healthy
            "Vietnamese Coffee Blend": 2.0,     # LOW STOCK (Below 5)
            "Full Cream Milk": 8.0,             # LOW STOCK (Below 20)
            "Oat Milk": 12.0,                   # Healthy
            "Premium Matcha Powder": 0.0,       # OUT OF STOCK (0)
            "Vanilla Syrup": 2.0,               # LOW STOCK (Below 5)
            "Butterscotch Sauce": 6.0,          # Healthy
            "Auro Chocolate Powder": 10.0,      # Healthy
            "16oz Plastic Cups (Iced)": 150.0,  # LOW STOCK (Below 300)
            "500ml Glass Jars": 250.0           # Healthy
        }

        for name, qty in stock_levels.items():
            if qty > 0:
                # Use manual_stock_in to bump the quantity up from the default 0
                stock_in(ingredient_ids[name], qty, user_id, "Manual", None, "Initial System Seeding")

        # --- 5. SAMPLE PURCHASE ORDER ---
        print("Creating a sample Purchase Order...")
        po_items = [
            {"item_id": ingredient_ids["Premium Matcha Powder"], "qty": 5, "unit_cost": 900.00},
            {"item_id": ingredient_ids["Vanilla Syrup"], "qty": 10, "unit_cost": 320.00}
        ]
        # Create a pending order for Sweet Syrups Inc.
        create_purchase_order(suppliers["Sweet Syrups Inc."], user_id, "2026-07-15", po_items)

        print("✅ Success! Database fully populated with realistic BFC Menu data!")

    except Exception as e:
        print(f"❌ An error occurred while seeding: {e}")

if __name__ == "__main__":
    seed_database()