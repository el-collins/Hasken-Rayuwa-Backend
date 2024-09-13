import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from core.config import settings
import uuid

def pg_to_sqlite_type(pg_type):
    type_mapping = {
        'integer': 'INTEGER',
        'bigint': 'INTEGER',
        'smallint': 'INTEGER',
        'character varying': 'TEXT',
        'text': 'TEXT',
        'boolean': 'INTEGER',
        'timestamp without time zone': 'TEXT',
        'date': 'TEXT',
        'numeric': 'REAL',
        'double precision': 'REAL',
        'uuid': 'TEXT',
        'USER-DEFINED': 'TEXT'  # For enum types
    }
    return type_mapping.get(pg_type, 'TEXT')

def adapt_value(value, pg_type):
    if value is None:
        return None
    if pg_type == 'uuid':
        return str(value)
    if pg_type == 'USER-DEFINED':  # For enum types
        return str(value)
    if pg_type.startswith('timestamp'):
        return value.isoformat()
    if pg_type == 'date':
        return value.isoformat()
    return value

def migrate_data():
    # PostgreSQL connection
    pg_conn = psycopg2.connect(settings.REMOTE_DATABASE_URL)
    pg_cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    # SQLite connection
    sqlite_conn = sqlite3.connect(settings.LOCAL_DATABASE_URL.replace('sqlite:///', ''))
    sqlite_cursor = sqlite_conn.cursor()

    # Enable foreign key support in SQLite
    sqlite_cursor.execute("PRAGMA foreign_keys = ON")

    # Get list of tables
    pg_cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    """)
    tables = pg_cursor.fetchall()

    for table in tables:
        table_name = table['table_name']
        print(f"Migrating table: {table_name}")

        # Get column information
        pg_cursor.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
        """)
        columns = pg_cursor.fetchall()

        # Create table in SQLite
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        create_table_sql += ", ".join([
            f"{col['column_name']} {pg_to_sqlite_type(col['data_type'])} "
            f"{'NOT NULL' if col['is_nullable'] == 'NO' else ''} "
            f"{'PRIMARY KEY' if col['column_default'] and 'uuid_generate_v4()' in col['column_default'] else ''}"
            for col in columns
        ])
        create_table_sql += ")"
        sqlite_cursor.execute(create_table_sql)

        # Fetch data from PostgreSQL
        pg_cursor.execute(f"SELECT * FROM {table_name}")
        rows = pg_cursor.fetchall()

        if rows:
            # Insert data into SQLite
            placeholders = ", ".join(["?" for _ in columns])
            insert_sql = f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})"
            sqlite_cursor.executemany(insert_sql, [
                tuple(adapt_value(row[col['column_name']], col['data_type']) for col in columns)
                for row in rows
            ])

    sqlite_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()

    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_data()