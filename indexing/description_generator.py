"""
Generate semantic descriptions for tables using LLM
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent.prompts import SCHEMA_DESCRIPTION_PROMPT
from config import DESCRIPTION_MODEL, TEMPERATURE


class DescriptionGenerator:
    """
    Generates business-oriented descriptions of database tables
    """
    
    def __init__(self):
        """Initialize the description generator"""
        self.llm = ChatGroq(
            model=DESCRIPTION_MODEL,
            temperature=TEMPERATURE + 0.3  # Slightly more creative for descriptions
        )
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SCHEMA_DESCRIPTION_PROMPT),
            ("user", "Here's a database table schema with sample rows:\n\n{schema}\n\nGenerate a business-focused description.")
        ])
        
        print("✓ Description generator initialized")
    
    def generate(self, table_info):
        """
        Generate semantic description for a table
        
        Args:
            table_info: Dictionary with 'table_name' and 'schema'
        
        Returns:
            String containing the business description
        """
        table_name = table_info['table_name']
        schema = table_info['schema']
        
        # Call LLM to generate description
        messages = self.prompt.format_messages(schema=schema)
        response = self.llm.invoke(messages)
        
        description = response.content.strip()
        
        return description
    
    def generate_batch(self, tables_info):
        """
        Generate descriptions for multiple tables
        
        Args:
            tables_info: List of table info dictionaries
        
        Returns:
            List of dictionaries with table_name and description
        """
        results = []
        
        for i, table_info in enumerate(tables_info, 1):
            table_name = table_info['table_name']
            print(f"  [{i}/{len(tables_info)}] Generating description for {table_name}...")
            
            description = self.generate(table_info)
            
            results.append({
                "table_name": table_name,
                "description": description
            })
        
        return results


# Test the generator
# if __name__ == "__main__":
#     from database.connection import get_db
#     from indexing.schema_extractor import SchemaExtractor
    
#     print("=" * 60)
#     print("TESTING DESCRIPTION GENERATOR")
#     print("=" * 60)
    
#     # Get database and extract schema
#     db = get_db()
#     extractor = SchemaExtractor(db)
    
#     # Get schema for first table
#     tables = extractor._get_table_list()
#     if tables:
#         print(f"\nGenerating description for: {tables[0]}")
#         table_info = extractor.extract_table(tables[0])
        
#         # Generate description
#         generator = DescriptionGenerator()
#         description = generator.generate(table_info)
        
#         print("\n" + "=" * 60)
#         print(f"DESCRIPTION FOR {tables[0].upper()}")
#         print("=" * 60)
#         print(description)
#         print("=" * 60)
        
#         print("\n✓ Description generated successfully!")
#     else:
#         print("No tables found in database")