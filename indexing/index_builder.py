

"""
Build and manage FAISS vector index for semantic search
"""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config import EMBEDDING_MODEL, VECTOR_INDEX_PATH, METADATA_PATH
from utils.helpers import save_json, load_json


class IndexBuilder:
    """
    Builds and manages the FAISS vector index for table descriptions
    """
    
    def __init__(self):
        """Initialize the index builder"""
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        print("✓ Index builder initialized")
    
    def build_index(self, table_descriptions):
        """
        Build FAISS index from table descriptions
        
        Args:
            table_descriptions: List of dicts with 'table_name' and 'description'
        
        Returns:
            FAISS vectorstore
        """
        print(f"\n📊 Building FAISS index for {len(table_descriptions)} tables...")
        
        # Convert to LangChain Document format
        documents = []
        for item in table_descriptions:
            doc = Document(
                page_content=item['description'],
                metadata={
                    "table_name": item['table_name'],
                    "source": "database_schema"
                }
            )
            documents.append(doc)
        
        # Build FAISS index
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        
        print(f"✓ FAISS index built with {len(documents)} tables")
        
        return vectorstore
    
    def save_index(self, vectorstore, metadata):
        """
        Save FAISS index and metadata to disk
        
        Args:
            vectorstore: FAISS vectorstore to save
            metadata: Table descriptions metadata
        """
        print("\n💾 Saving index to disk...")
        
        # Save FAISS index
        vectorstore.save_local(str(VECTOR_INDEX_PATH))
        print(f"✓ Saved FAISS index to {VECTOR_INDEX_PATH}")
        
        # Save metadata (for human inspection)
        save_json(metadata, METADATA_PATH)
        print(f"✓ Saved metadata to {METADATA_PATH}")
    
    @staticmethod
    def load_index():
        """
        Load FAISS index from disk
        
        Returns:
            FAISS vectorstore
        """
        print("📂 Loading FAISS index from disk...")
        
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        
        try:
            vectorstore = FAISS.load_local(
                str(VECTOR_INDEX_PATH),
                embeddings,
                allow_dangerous_deserialization=True  # Required for FAISS
            )
            print("✓ Index loaded successfully")
            return vectorstore
        
        except Exception as e:
            raise FileNotFoundError(
                f"Could not load index from {VECTOR_INDEX_PATH}\n"
                f"Error: {e}\n"
                f"Please run: python setup_index.py"
            )
    
    @staticmethod
    def load_metadata():
        """
        Load metadata from disk
        
        Returns:
            List of table descriptions
        """
        try:
            return load_json(METADATA_PATH)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Metadata not found at {METADATA_PATH}\n"
                f"Please run: python setup_index.py"
            )


# Test the index builder
# if __name__ == "__main__":
#     print("=" * 60)
#     print("TESTING INDEX BUILDER")
#     print("=" * 60)
    
#     # Create sample descriptions
#     sample_descriptions = [
#         {
#             "table_name": "orders",
#             "description": "The orders table stores all customer purchase transactions. It contains order IDs, customer references, order dates, and total amounts. Use this table to analyze sales revenue, order counts, and purchase patterns over time."
#         },
#         {
#             "table_name": "customers",
#             "description": "The customers table stores customer master data including contact information and registration details. It contains customer IDs, email addresses, and signup dates. Use this table for customer analytics, user growth tracking, and demographic analysis."
#         },
#         {
#             "table_name": "products",
#             "description": "The products table contains the product catalog with product names, descriptions, and prices. It includes product IDs, categories, and inventory levels. Use this table for product performance analysis and inventory management."
#         }
#     ]
    
#     # Build index
#     builder = IndexBuilder()
#     vectorstore = builder.build_index(sample_descriptions)
    
#     # Save index
#     builder.save_index(vectorstore, sample_descriptions)
    
#     print("\n" + "=" * 60)
#     print("Testing index loading...")
#     print("=" * 60)
    
#     # Test loading
#     loaded_vectorstore = IndexBuilder.load_index()
#     loaded_metadata = IndexBuilder.load_metadata()
    
#     print(f"✓ Loaded index with {len(loaded_metadata)} tables")
    
#     # Test search
#     print("\n" + "=" * 60)
#     print("Testing semantic search...")
#     print("=" * 60)
    
#     test_query = "Show me customer data"
#     results = loaded_vectorstore.similarity_search(test_query, k=2)
    
#     print(f"\nQuery: '{test_query}'")
#     print("Top results:")
#     for i, doc in enumerate(results, 1):
#         print(f"{i}. {doc.metadata['table_name']}")
    
#     print("\n✓ Index builder working correctly!")