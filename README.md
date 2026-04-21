# NLP to SQL Query System using LLMs

##  Overview
This project enables users to query a structured financial database using natural language.

It leverages Large Language Models (LLMs) to convert user queries into SQL, execute them, and return results with explanations.

The system is designed to be robust, safe, and interpretable.

---

##  Features
- Natural Language → SQL conversion
- Semantic understanding of business queries
- SQL validation (prevents unsafe queries)
- Retry mechanism for failed queries
- Query explanation generation
- Logging for observability
- Ambiguity handling

---

##  Tech Stack
- Python
- SQLite
- LLM (Groq / OpenAI)
- Pandas

---

##  Architecture
User Query → Prompt Builder → LLM → SQL Generator → Validator → Executor → Result + Explanation

---

##  Example

**Input:**
How many invoices are there?

**Generated SQL:**
```sql
SELECT COUNT(*) FROM invoices;

Output:
101

Explanation:
Counts total number of invoices in the database.

## Key Highlights
- Built end-to-end NLP → SQL pipeline
- Implemented query validation to prevent unsafe SQL
- Handled ambiguous queries with clarification
- Integrated LLM with structured database execution
