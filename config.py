import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

# Root of the project (where this file lives)
PROJECT_ROOT = Path(__file__).resolve().parent

# Database path (from env or default)
DB_PATH = Path(os.getenv("DATABASE_PATH", PROJECT_ROOT / "database" / "olist_ecommerce.sqlite"))
DB_URL = f"sqlite:///{DB_PATH}"

# Vector Index Storage
VECTOR_INDEX_DIR = PROJECT_ROOT / "indexing" / "metadata"
VECTOR_INDEX_PATH = VECTOR_INDEX_DIR / "schema_index"
METADATA_PATH = VECTOR_INDEX_DIR / "table_descriptions.json"

# Ensure required directories exist
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# API Keys
# ---------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------------------------------------------
# Model Configuration
# ---------------------------------------------------

# LLM for SQL generation (primary)
SQL_GENERATION_MODEL = "openai/gpt-oss-120b"

# LLM for description generation
DESCRIPTION_MODEL = "openai/gpt-oss-120b"

# LLM for answer formatting
ANSWER_MODEL = "openai/gpt-oss-120b"

# Embedding model for vector search
EMBEDDING_MODEL = "text-embedding-3-small"
# EMBEDDING_MODEL = "models/gemini-embedding-001"

# ---------------------------------------------------
# Agent Settings
# ---------------------------------------------------
MAX_TABLES_IN_CONTEXT = 3              # Number of tables in prompt context
SQL_TIMEOUT_SECONDS = 30               # Query timeout
MAX_RESULT_ROWS = 1000                 # Cap result size
TEMPERATURE = 0                        # Deterministic LLM output

# ---------------------------------------------------
# Indexing Settings
# ---------------------------------------------------
SAMPLE_ROWS_FOR_DESCRIPTION = 3

# ---------------------------------------------------
# Debug Info
# ---------------------------------------------------
# if __name__ == "__main__":
#     print("=" * 60)
#     print("CONFIGURATION")
#     print("=" * 60)
#     print(f"Project Root: {PROJECT_ROOT}")
#     print(f"Database Path: {DB_PATH}")
#     print(f"Database URL: {DB_URL}")
#     print(f"Vector Index Path: {VECTOR_INDEX_PATH}")
#     print(f"SQL Model: {SQL_GENERATION_MODEL}")
#     print(f"Description Model: {DESCRIPTION_MODEL}")
#     print(f"Embedding Model: {EMBEDDING_MODEL}")
#     print(f"Max Tables in Context: {MAX_TABLES_IN_CONTEXT}")
#     print("=" * 60)
