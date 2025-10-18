"""
Semantic retrieval of relevant tables for a query
"""
from config import MAX_TABLES_IN_CONTEXT


class SchemaRetriever:
    """
    Retrieves relevant tables using semantic search
    """
    
    def __init__(self, vectorstore):
        """
        Initialize the retriever
        
        Args:
            vectorstore: FAISS vectorstore with table descriptions
        """
        self.vectorstore = vectorstore
        print("✓ Schema retriever initialized")
    
    def retrieve_tables(self, query, k=None):
        """
        Find most relevant tables for a query
        
        Args:
            query: User's natural language query
            k: Number of tables to retrieve (default from config)
        
        Returns:
            List of table names
        """
        if k is None:
            k = MAX_TABLES_IN_CONTEXT
        
        # Semantic search in vector store
        results = self.vectorstore.similarity_search(query, k=k)
        
        # Extract table names from results
        table_names = [doc.metadata['table_name'] for doc in results]
        
        print(f"🔍 Retrieved tables for '{query}': {table_names}")
        
        return table_names
    
    def retrieve_with_scores(self, query, k=None):
        """
        Retrieve tables with similarity scores
        
        Args:
            query: User's natural language query
            k: Number of tables to retrieve
        
        Returns:
            List of tuples (table_name, score)
        """
        if k is None:
            k = MAX_TABLES_IN_CONTEXT
        
        # Get results with scores
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # Format as list of tuples
        tables_with_scores = [
            (doc.metadata['table_name'], score) 
            for doc, score in results
        ]
        
        print(f"🔍 Retrieved tables with scores:")
        for table, score in tables_with_scores:
            print(f"   {table}: {score:.3f}")
        
        return tables_with_scores


# Test the retriever
# if __name__ == "__main__":
#     from indexing.index_builder import IndexBuilder
    
#     print("=" * 60)
#     print("TESTING SCHEMA RETRIEVER")
#     print("=" * 60)
    
#     # Load index
#     print("\nLoading index...")
#     vectorstore = IndexBuilder.load_index()
    
#     # Create retriever
#     retriever = SchemaRetriever(vectorstore)
    
#     # Test queries
#     test_queries = [
#         "Show me customer information",
#         "What is our total revenue?",
#         "How many orders were placed?",
#         "Which products are selling best?"
#     ]
    
#     print("\n" + "=" * 60)
#     print("TESTING QUERIES")
#     print("=" * 60)
    
#     for query in test_queries:
#         print(f"\n📝 Query: '{query}'")
#         tables = retriever.retrieve_tables(query, k=2)
#         print(f"   Tables: {tables}")
    
#     print("\n" + "=" * 60)
#     print("TESTING WITH SCORES")
#     print("=" * 60)
    
#     query = "Show me sales data"
#     print(f"\n📝 Query: '{query}'")
#     tables_with_scores = retriever.retrieve_with_scores(query, k=3)
    
#     print("\n✓ Retriever working correctly!")