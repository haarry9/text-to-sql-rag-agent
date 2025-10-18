"""
Extract database schema using LangChain tools
"""

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from config import DESCRIPTION_MODEL

class SchemaExtractor:
    """
    Extract database schema using LangChain tools
    """
    
    def __init__(self, db):
        """
        Initialize with a LangChain SQLDatabase instance
        
        Args:
            db: LangChain SQLDatabase object
        """
        self.db = db
        llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm)
        self.tools = {tool.name: tool for tool in self.toolkit.get_tools()}
        
        print("✓ Schema extractor initialized")
    
    def extract_all_tables(self):
        """
        Extract schema information for all tables
        
        Returns:
            List of dictionaries, each containing table schema info
        """
        print("\n📋 Extracting schema for all tables...")
        
        # Step 1: Get list of all table names
        table_names = self._get_table_list()
        print(f"Found {len(table_names)} tables: {table_names}")
        
        # Step 2: Get detailed schema for each table
        tables_info = []
        for i, table_name in enumerate(table_names, 1):
            print(f"  [{i}/{len(table_names)}] Extracting {table_name}...")
            table_info = self.extract_table(table_name)
            tables_info.append(table_info)
        
        print(f"✓ Extracted schema for {len(tables_info)} tables")
        return tables_info
    
    def extract_table(self, table_name):
        """
        Extract schema for a single table
        
        Args:
            table_name: Name of the table
        
        Returns:
            Dictionary with table schema information
        """
        # Use LangChain's sql_db_schema tool
        schema_tool = self.tools['sql_db_schema']
        
        # Get schema with sample rows
        schema_info = schema_tool.invoke(table_name)
        
        return {
            "table_name": table_name,
            "schema": schema_info,  # This is the formatted DDL + samples
        }
    
    def _get_table_list(self):
        """
        Get list of all table names using LangChain tool
        
        Returns:
            List of table names
        """
        list_tables_tool = self.tools['sql_db_list_tables']
        
        # Tool expects empty string as input
        result = list_tables_tool.invoke("")
        
        # Result is comma-separated string like "table1, table2, table3"
        tables = [t.strip() for t in result.split(',') if t.strip()]
        
        return tables
    
# Test the extractor
# if __name__ == "__main__":
#     from database.connection import get_db
    
#     print("=" * 60)
#     print("TESTING SCHEMA EXTRACTOR")
#     print("=" * 60)
    
#     # Get database connection
#     db = get_db()
    
#     # Create extractor
#     extractor = SchemaExtractor(db)
    
#     # Test getting table list
#     print("\nTest 1: Get table list")
#     tables = extractor._get_table_list()
#     print(f"Tables: {tables}")
    
#     # Test extracting single table
#     print("\nTest 2: Extract single table")
#     if tables:
#         table_info = extractor.extract_table(tables[0])
#         print(f"\nSchema for {tables[0]}:")
#         print(table_info['schema'][:500] + "...")
    
#     # Test extracting all tables
#     print("\nTest 3: Extract all tables")
#     all_tables = extractor.extract_all_tables()
#     print(f"\n✓ Successfully extracted {len(all_tables)} tables")