"""
Application-wide configuration.
Reads DB credentials from a .env file (create one in the project root):

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=supply_management_db
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Database ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "supply_management_db")

# --- App ---
#APP_NAME = "Supply & Inventory Management System"
#APP_VERSION = "1.0.0"
#APP_THEME = "flatly"          # ttkbootstrap theme name (try 'darkly', 'cosmo', 'superhero')
#WINDOW_SIZE = "1200x720"

# --- Business rules ---
DEFAULT_REORDER_LEVEL = 10    # fallback reorder threshold if item has none set

# --- Roles ---
ROLE_ADMIN = "admin"
ROLE_STAFF = "staff"