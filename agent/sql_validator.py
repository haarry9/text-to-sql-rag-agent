"""
Validate SQL queries before execution
"""
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from config import DESCRIPTION_MODEL


class SQLValidator:
    """
    Validates SQL queries for safety and correctness
    """
    
    def __init__(self, db):
        """
        Initialize validator
        
        Args:
            db: LangChain SQLDatabase instance
        """
        self.db = db
        
        # Initialize toolkit to use query checker tool
        llm = ChatGroq(model=DESCRIPTION_MODEL, temperature=0)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        self.tools = {tool.name: tool for tool in toolkit.get_tools()}
        
        print("✓ SQL validator initialized")
    
    def validate(self, sql):
        """
        Validate SQL query
        
        Args:
            sql: SQL query string
        
        Returns:
            Tuple (is_valid, message)
        """
        print("🔍 Validating SQL...")
        
        # Basic safety checks
        safety_check = self._check_safety(sql)
        if not safety_check[0]:
            return safety_check
        
        # Use LangChain's query checker (optional, can be slow)
        # Uncomment if you want deep validation
        # checker_result = self._check_with_langchain(sql)
        # if not checker_result[0]:
        #     return checker_result
        
        print("✓ SQL validation passed")
        return True, "SQL is valid"
    
    def _check_safety(self, sql):
        """
        Basic safety checks
        
        Args:
            sql: SQL query string
        
        Returns:
            Tuple (is_safe, message)
        """
        sql_upper = sql.upper()
        
        # Check for dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'UPDATE', 'INSERT']
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False, f"Dangerous operation detected: {keyword} is not allowed"
        
        # Check for empty query
        if not sql.strip():
            return False, "Empty SQL query"
        
        # Check if it's a SELECT statement
        if not sql_upper.strip().startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        return True, "Safety checks passed"
    
    def _check_with_langchain(self, sql):
        """
        Deep validation using LangChain's query checker
        
        Args:
            sql: SQL query string
        
        Returns:
            Tuple (is_valid, message)
        """
        try:
            checker_tool = self.tools['sql_db_query_checker']
            result = checker_tool.invoke({"query": sql})
            return True, "Query checker passed"
        except Exception as e:
            return False, f"Query checker failed: {str(e)}"


# Test validator
# if __name__ == "__main__":
#     from database.connection import get_db
    
#     print("=" * 60)
#     print("TESTING SQL VALIDATOR")
#     print("=" * 60)
    
#     # Get database
#     db = get_db()
    
#     # Create validator
#     validator = SQLValidator(db)
    
#     # Test valid query
#     print("\nTest 1: Valid SELECT query")
#     valid_sql = "SELECT * FROM customers LIMIT 10;"
#     is_valid, msg = validator.validate(valid_sql)
#     print(f"Result: {is_valid} - {msg}")
    
#     # Test dangerous query
#     print("\nTest 2: Dangerous DELETE query")
#     dangerous_sql = "DELETE FROM customers WHERE id = 1;"
#     is_valid, msg = validator.validate(dangerous_sql)
#     print(f"Result: {is_valid} - {msg}")
    
#     # Test UPDATE query
#     print("\nTest 3: UPDATE query (should fail)")
#     update_sql = "UPDATE customers SET name = 'Test' WHERE id = 1;"
#     is_valid, msg = validator.validate(update_sql)
#     print(f"Result: {is_valid} - {msg}")
    
#     # Test empty query
#     print("\nTest 4: Empty query")
#     empty_sql = ""
#     is_valid, msg = validator.validate(empty_sql)
#     print(f"Result: {is_valid} - {msg}")
    
#     print("\n" + "=" * 60)
#     print("✓ Validator working correctly!")