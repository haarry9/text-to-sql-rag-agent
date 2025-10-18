# from sqlalchemy import create_engine, text
# import pathlib

# # Correct relative path to your file
# db_path = pathlib.Path("database/olist_ecommerce.sqlite")

# engine = create_engine(f"sqlite:///{db_path}")

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
#     tables = [row[0] for row in result]
#     print("Tables in DB:", tables)


# from langchain_community.utilities import SQLDatabase

# db = SQLDatabase.from_uri("sqlite:///database/olist_ecommerce.sqlite")

# print(f"Dialect: {db.dialect}")
# print(f"Available tables: {db.get_usable_table_names()}")
# print(f'Sample output: {db.run("SELECT * FROM customers LIMIT 5;")}')

from langchain_community.utilities import SQLDatabase
from config import DB_PATH, DB_URL

db = SQLDatabase.from_uri(DB_URL)

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM customers LIMIT 5;")}')

def get_db():
    """
    Get LangChain SQLDatabase instance
    
    Returns:
        SQLDatabase object connected to our database
    """
    # Check if database file exists
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}\n"
            f"Please copy your ecommerce.sqlite file to the database/ folder"
        )
    
    # Create SQLDatabase instance
    db = SQLDatabase.from_uri(DB_URL)
    
    return db

def get_db_with_tables(include_tables=None):
    """
    Get SQLDatabase with only specific tables visible
    Useful for limiting context to relevant tables
    
    Args:
        include_tables: List of table names to include
    
    Returns:
        SQLDatabase with filtered tables
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    else:
        db = get_db()
    
    # Filter to include only specified tables
    db.include_tables = include_tables
    
    return db

def test_connection():
    """
    Test the database connection
    """
    print("Testing database connection...")
    
    try:
        db = get_db()
        print(f"✓ Connected to database at {DB_PATH}")
        
        # Get table names
        table_names = db.get_table_names()
        print(f"✓ Found {len(table_names)} tables:")
        for table in table_names:
            print(f"  - {table}")
        
        # Run a simple query
        result = db.run("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table';")
        print(f"✓ Query test successful: {result}")
        
        print("\n✓ Database connection working!")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


# Run test when executed directly
if __name__ == "__main__":
    test_connection()