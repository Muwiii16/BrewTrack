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
DB_NAME = os.getenv("DB_NAME", "brewtrack_db")