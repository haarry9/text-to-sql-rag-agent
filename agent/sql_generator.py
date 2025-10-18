"""
Generate SQL queries using LLM
"""
from langchain_groq import ChatGroq
from agent.prompts import SQL_GENERATION_PROMPT
from config import SQL_GENERATION_MODEL, TEMPERATURE
from utils.helpers import clean_sql


class SQLGenerator:
    """
    Generates SQL queries from natural language questions
    """
    
    def __init__(self):
        """Initialize SQL generator"""
        self.llm = ChatGroq(
            model=SQL_GENERATION_MODEL,
            temperature=TEMPERATURE
        )
        print("✓ SQL generator initialized")
    
    def generate(self, question, schema_context):
        """
        Generate SQL query from question and schema
        
        Args:
            question: User's natural language question
            schema_context: Database schema for relevant tables
        
        Returns:
            SQL query string
        """
        print(f"💻 Generating SQL for: '{question}'")
        
        # Format prompt
        prompt = SQL_GENERATION_PROMPT.format(
            schema=schema_context,
            question=question
        )
        
        # Call LLM
        response = self.llm.invoke(prompt)
        
        # Clean up the SQL
        sql = clean_sql(response.content)
        
        print(f"✓ Generated SQL ({len(sql)} characters)")
        
        return sql


# Test SQL generator
# if __name__ == "__main__":
#     print("=" * 60)
#     print("TESTING SQL GENERATOR")
#     print("=" * 60)
    
#     # Create sample schema
#     sample_schema = """
# CREATE TABLE customers (
#     customer_id INTEGER PRIMARY KEY,
#     email TEXT NOT NULL,
#     name TEXT,
#     created_at DATE
# );

# /*
# 3 rows from customers table:
# customer_id  email               name          created_at
# 1            john@example.com    John Doe      2024-01-15
# 2            sarah@test.com      Sarah Smith   2024-01-16
# 3            mike@company.com    Mike Johnson  2024-01-17
# */

# CREATE TABLE orders (
#     order_id INTEGER PRIMARY KEY,
#     customer_id INTEGER,
#     order_date DATE,
#     total_amount DECIMAL(10,2),
#     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
# );

# /*
# 3 rows from orders table:
# order_id  customer_id  order_date  total_amount
# 1         1            2024-01-20  99.99
# 2         1            2024-01-22  149.50
# 3         2            2024-01-21  75.00
# */
# """
    
#     # Test questions
#     test_questions = [
#         "How many customers do we have?",
#         "What is the total revenue?",
#         "Show me the top 5 customers by order count",
#         "What was the average order value last month?"
#     ]
    
#     # Create generator
#     generator = SQLGenerator()
    
#     # Test each question
#     for i, question in enumerate(test_questions, 1):
#         print(f"\n{'='*60}")
#         print(f"TEST {i}: {question}")
#         print('='*60)
        
#         sql = generator.generate(question, sample_schema)
        
#         print(f"\nGenerated SQL:")
#         print(sql)
    
#     print("\n" + "=" * 60)
#     print("✓ SQL generator working!")