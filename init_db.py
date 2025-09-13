#!/usr/bin/env python3
"""Database initialization script for Lost & Found Web App"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import User, Item

def init_db():
    """Initialize the database with all tables"""
    print("Creating database tables...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")
        
        return True

if __name__ == '__main__':
    try:
        success = init_db()
        if success:
            print("\n🎉 Database initialization completed!")
            print("You can now run the Flask application.")
        else:
            print("\n❌ Database initialization failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error initializing database: {e}")
        sys.exit(1)
