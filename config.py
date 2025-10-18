import os
import pathlib as Path
from dotenv import load_dotenv

load_dotenv()

"""
Environment variables loading
Database path
Model names
"""

DB_PATH = Path.Path(os.getenv("DATABASE_PATH", "database/olist_ecommerce.sqlite"))
DB_URL = f"sqlite:///{DB_PATH}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MODEL CONFIGURATION
# LLM for SQL generation (needs to be good at SQL)
SQL_GENERATION_MODEL = "openai/gpt-oss-120b"

# LLM for description generation (can be cheaper)
DESCRIPTION_MODEL = "openai/gpt-oss-120b"

# LLM for answer formatting (can be cheaper)
ANSWER_MODEL = "openai/gpt-oss-120b"

# Embedding model for vector search
EMBEDDING_MODEL = "text-embedding-3-small"

# AGENT SETTINGS
# Maximum number of tables to include in context
MAX_TABLES_IN_CONTEXT = 3

# SQL execution timeout (seconds)
SQL_TIMEOUT_SECONDS = 30

# Maximum rows to return from query
MAX_RESULT_ROWS = 1000

# Temperature for LLM calls
TEMPERATURE = 0


# INDEXING SETTINGS
# Number of sample rows to include in schema descriptions
SAMPLE_ROWS_FOR_DESCRIPTION = 3
