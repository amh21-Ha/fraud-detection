import sys
import os

# Add your project directory to the Python path
project_home = '../fraud-detection'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the FastAPI app
from app.main import app

# Create tables and ensure everything is set up
from app.database import create_tables
create_tables()

# This is the WSGI callable that PythonAnyWhere will use
application = app