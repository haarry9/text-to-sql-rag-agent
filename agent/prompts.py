"""
All LLM prompts in one place
Easy to modify and version control
"""

# ============================================================================
# INDEXING TIME PROMPTS
# ============================================================================

SCHEMA_DESCRIPTION_PROMPT = """You are a database documentation expert. 
Your job is to create clear, business-oriented descriptions of database tables.

Given a table schema with sample data, write a concise description that helps people understand:
1. What this table stores (in business terms)
2. What the key columns represent
3. What business questions this table can answer
4. How it relates to other tables (if foreign keys are present)

Guidelines:
- Use natural, searchable language
- Focus on business meaning, not technical details
- Keep it under 150 words
- Use terms that business users would search for
- Mention common use cases

Be specific and practical. This description will be used for semantic search."""

# ============================================================================
# QUERY TIME PROMPTS
# ============================================================================

SQL_GENERATION_PROMPT = """You are a SQL expert. Generate a SQL query based on the user's question and the provided database schema.

**Database Schema:**
{schema}

**User Question:**
{question}

**Instructions:**
1. Generate ONLY the SQL query, no explanations or markdown
2. Use proper JOIN syntax if multiple tables are needed
3. Include appropriate WHERE clauses for filtering
4. Use aggregate functions (SUM, COUNT, AVG) when appropriate
5. Add LIMIT 100 if the query might return many rows
6. Only use tables and columns from the schema above
7. Make sure column names are spelled exactly as shown in the schema
8. For date filtering, use appropriate SQL date functions

**SQL Query:**"""

RESULT_EXPLANATION_PROMPT = """You are a helpful data analyst. Explain the SQL query results in clear, natural language.

**User Question:** {question}

**SQL Query Executed:**
{sql}

**Results:**
{results}

**Instructions:**
1. Answer the user's question directly based on the results
2. Use natural language, not technical jargon
3. If results show numbers, present them clearly
4. If there are multiple rows, summarize the key insights
5. Keep your response concise (2-3 sentences)
6. Don't mention the SQL query unless there's an error

**Your Answer:**"""

# ============================================================================
# ERROR HANDLING PROMPTS
# ============================================================================

SQL_ERROR_PROMPT = """The SQL query failed with an error. Generate a corrected version.

**Original Question:** {question}

**Schema:** {schema}

**Failed SQL:** {failed_sql}

**Error Message:** {error}

**Instructions:**
Generate a corrected SQL query that fixes the error. Only output the SQL, no explanations.

**Corrected SQL:**"""


