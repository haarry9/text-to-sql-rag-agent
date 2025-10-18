"""
One-time setup script to index database schema
Run this before using the agent: python setup_index.py
"""
from database.connection import get_db
from indexing.schema_extractor import SchemaExtractor
from indexing.description_generator import DescriptionGenerator
from indexing.index_builder import IndexBuilder


def main():
    """Main indexing pipeline"""
    
    print("=" * 60)
    print("🚀 SETTING UP SCHEMA INDEX")
    print("=" * 60)
    
    # Step 1: Connect to database
    print("\n📦 Step 1: Connecting to database...")
    try:
        db = get_db()
        print("✓ Connected successfully")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return
    
    # Step 2: Extract schema using LangChain tools
    print("\n📋 Step 2: Extracting schema with LangChain tools...")
    try:
        extractor = SchemaExtractor(db)
        tables_schema = extractor.extract_all_tables()
        print(f"✓ Extracted {len(tables_schema)} tables")
    except Exception as e:
        print(f"✗ Schema extraction failed: {e}")
        return
    
    # Step 3: Generate semantic descriptions
    print("\n🤖 Step 3: Generating semantic descriptions with LLM...")
    print("(This may take a few minutes...)")
    try:
        generator = DescriptionGenerator()
        table_descriptions = generator.generate_batch(tables_schema)
        print(f"✓ Generated descriptions for {len(table_descriptions)} tables")
    except Exception as e:
        print(f"✗ Description generation failed: {e}")
        return
    
    # Step 4: Build vector index
    print("\n📊 Step 4: Building FAISS vector index...")
    try:
        builder = IndexBuilder()
        vectorstore = builder.build_index(table_descriptions)
        print("✓ Index built successfully")
    except Exception as e:
        print(f"✗ Index building failed: {e}")
        return
    
    # Step 5: Save to disk
    print("\n💾 Step 5: Saving index to disk...")
    try:
        builder.save_index(vectorstore, table_descriptions)
        print("✓ Index saved successfully")
    except Exception as e:
        print(f"✗ Saving failed: {e}")
        return
    
    # Success!
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now run the agent:")
    print("  streamlit run main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()