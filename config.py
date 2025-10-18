import os
import pathlib as Path
from dotenv import load_dotenv

load_dotenv()

"""
Environment variables loading
Database path
Model names
"""

DATABASE_PATH = Path.Path(os.getenv("DATABASE_PATH", "database/olist_ecommerce.sqlite"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-large")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
print(f"Database Path: {DATABASE_PATH}")    
