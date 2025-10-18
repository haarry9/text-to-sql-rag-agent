"""
Build minimal schema context for SQL generation
"""
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from config import DESCRIPTION_MODEL


"""
Build minimal schema context for SQL generation
"""
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from config import DESCRIPTION_MODEL


class ContextBuilder:
    """
    Builds minimal schema context for selected tables
    """
    
    def __init__(self, db):
        """
        Initialize context builder
        
        Args:
            db: LangChain SQLDatabase instance
        """
        self.db = db
        
        # Initialize toolkit to use sql_db_schema tool
        llm = ChatGroq(model=DESCRIPTION_MODEL, temperature=0)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        self.tools = {tool.name: tool for tool in toolkit.get_tools()}
        
        print("✓ Context builder initialized")
    
    def build_context(self, table_names):
        """
        Build schema context for selected tables
        
        Args:
            table_names: List of table names to include
        
        Returns:
            String with DDL and sample rows for selected tables
        """
        if not table_names:
            return "No tables selected."
        
        print(f"📝 Building context for tables: {table_names}")
        
        # Use LangChain's sql_db_schema tool
        schema_tool = self.tools['sql_db_schema']
        
        # Tool expects comma-separated table names
        tables_str = ", ".join(table_names)
        
        # Get schema with sample rows
        schema_context = schema_tool.invoke(tables_str)
        
        return schema_context
    
    def build_context_with_relationships(self, table_names):
        """
        Build context with explicit relationship information
        (Optional enhancement)
        
        Args:
            table_names: List of table names
        
        Returns:
            Schema context with relationship hints
        """
        # Get basic schema
        context = self.build_context(table_names)
        
        # Add relationship hints if multiple tables
        if len(table_names) > 1:
            context += "\n\n-- HINT: These tables are related. Look for foreign key columns that reference other tables.\n"
        
        return context


# Test the context builder
# if __name__ == "__main__":
#     from database.connection import get_db
    
#     print("=" * 60)
#     print("TESTING CONTEXT BUILDER")
#     print("=" * 60)
    
#     # Get database
#     db = get_db()
    
#     # Create context builder
#     builder = ContextBuilder(db)
    
#     # Get list of tables
#     table_names = db.get_table_names()
    
#     if len(table_names) >= 2:
#         # Test with first 2 tables
#         test_tables = table_names[:2]
        
#         print(f"\nBuilding context for: {test_tables}")
#         print("\n" + "=" * 60)
        
#         context = builder.build_context(test_tables)
        
#         print(context)
        
#         print("\n" + "=" * 60)
#         print(f"✓ Context built ({len(context)} characters)")
#     else:
#         print("Need at least 2 tables to test")