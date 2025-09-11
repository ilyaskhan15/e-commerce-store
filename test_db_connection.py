#!/usr/bin/env python
"""Test database connection for debugging."""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_database_connection():
    """Test PostgreSQL database connection."""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return False
    
    print(f"Testing connection to: {database_url}")
    
    try:
        # Parse the database URL
        url = urlparse(database_url)
        print(f"Host: {url.hostname}")
        print(f"Port: {url.port}")
        print(f"Database: {url.path[1:]}")  # Remove leading slash
        print(f"Username: {url.username}")
        
        # Test connection
        print("Attempting to connect...")
        conn = psycopg2.connect(database_url)
        
        # Test simple query
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[0]}")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
