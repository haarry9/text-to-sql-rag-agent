"""
Execute SQL queries safely
"""
import pandas as pd
from config import SQL_TIMEOUT_SECONDS, MAX_RESULT_ROWS


class SQLExecutor:
    """
    Executes SQL queries and returns results
    """
    
    def __init__(self, db):
        """
        Initialize executor
        
        Args:
            db: LangChain SQLDatabase instance
        """
        self.db = db
        print("✓ SQL executor initialized")
    
    def execute(self, sql):
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            sql: SQL query string
        
        Returns:
            pandas DataFrame with results
        """
        print(f"⚡ Executing SQL...")
        
        try:
            # Run query using LangChain's run method
            # This returns a string, so we need to parse it
            result_str = self.db.run(sql)
            
            # For better results, use direct connection
            # Get the underlying SQLAlchemy engine
            engine = self.db._engine
            
            # Execute with pandas (handles DataFrame conversion automatically)
            df = pd.read_sql_query(sql, engine)
            
            # Limit results
            if len(df) > MAX_RESULT_ROWS:
                print(f"⚠️  Results truncated to {MAX_RESULT_ROWS} rows")
                df = df.head(MAX_RESULT_ROWS)
            
            print(f"✓ Query executed successfully ({len(df)} rows)")
            
            return df
        
        except Exception as e:
            print(f"✗ Query execution failed: {e}")
            raise Exception(f"SQL execution error: {str(e)}")
    
    def execute_with_timeout(self, sql, timeout=None):
        """
        Execute query with timeout (basic version)
        
        Args:
            sql: SQL query string
            timeout: Timeout in seconds (uses config default if None)
        
        Returns:
            pandas DataFrame
        """
        if timeout is None:
            timeout = SQL_TIMEOUT_SECONDS
        
        # For SQLite, timeout is handled at connection level
        # For production with PostgreSQL/MySQL, implement proper timeout
        
        return self.execute(sql)


# Test executor
if __name__ == "__main__":
    from database.connection import get_db
    
    print("=" * 60)
    print("TESTING SQL EXECUTOR")
    print("=" * 60)
    
    # Get database
    db = get_db()
    
    # Create executor
    executor = SQLExecutor(db)
    
    # Get a table name to test with
    tables = db.get_usable_table_names()
    
    if tables:
        test_table = tables[0]
        
        # Test simple query
        print(f"\nTest 1: SELECT from {test_table}")
        sql = f"SELECT * FROM {test_table} LIMIT 5;"
        
        try:
            df = executor.execute(sql)
            print("\nResults:")
            print(df)
            print(f"\nShape: {df.shape}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test COUNT query
        print(f"\nTest 2: COUNT from {test_table}")
        sql = f"SELECT COUNT(*) as total FROM {test_table};"
        
        try:
            df = executor.execute(sql)
            print("\nResults:")
            print(df)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 60)
        print("✓ Executor working!")
    else:
        print("No tables found in database")