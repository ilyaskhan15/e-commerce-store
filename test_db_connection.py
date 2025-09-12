#!/usr/bin/env python
"""Test database connection for debugging."""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_database_connection():
    """Test PostgreSQL database connection."""
    
    # Try DATABASE_URL first, then individual variables
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        print(f"Testing connection using DATABASE_URL: {database_url}")
        try:
            url = urlparse(database_url)
            print(f"Host: {url.hostname}")
            print(f"Port: {url.port}")
            print(f"Database: {url.path[1:]}")
            print(f"Username: {url.username}")
            
            conn = psycopg2.connect(database_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✅ Connection successful!")
                print(f"PostgreSQL version: {version[0]}")
            conn.close()
            return True
        except Exception as e:
            print(f"❌ DATABASE_URL connection failed: {e}")
    
    # Fallback to individual environment variables
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT', '5432')
    
    if not all([db_host, db_name, db_user, db_password]):
        print("❌ ERROR: Missing database environment variables")
        print("Required: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD")
        return False
    
    print(f"Testing connection using individual variables:")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Database: {db_name}")
    print(f"Username: {db_user}")
    
    try:
        # Try internal hostname first
        print(f"Attempting connection to {db_host}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[0]}")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed with internal hostname: {e}")
        
        # Try with full hostname
        full_hostname = f"{db_host}.render-postgres.render.com"
        print(f"Trying full hostname: {full_hostname}")
        
        try:
            conn = psycopg2.connect(
                host=full_hostname,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✅ Connection successful with full hostname!")
                print(f"PostgreSQL version: {version[0]}")
            
            conn.close()
            return True
            
        except Exception as e2:
            print(f"❌ Connection failed with full hostname: {e2}")
            return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
