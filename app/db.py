import os
import psycopg2
from psycopg2 import sql

# Prefer SUPABASE_URL if set, otherwise use individual credentials
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', 5432)

def get_connection():
    # Fallback to individual credentials
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def init_userfinancials_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS "UserFinancials" (
        session_id UUID PRIMARY KEY,
        gross_salary NUMERIC(15, 2),
        basic_salary NUMERIC(15, 2),
        hra_received NUMERIC(15, 2),
        rent_paid NUMERIC(15, 2),
        deduction_80c NUMERIC(15, 2),
        deduction_80d NUMERIC(15, 2),
        standard_deduction NUMERIC(15, 2),
        professional_tax NUMERIC(15, 2),
        tds NUMERIC(15, 2),
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    '''
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
    finally:
        conn.close() 