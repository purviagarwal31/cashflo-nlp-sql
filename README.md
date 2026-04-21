# 🚀 NLP to SQL Query System with Semantic Layer

## 📌 Overview
This project enables users to query a structured financial database using natural language.

It leverages Large Language Models (LLMs) along with a **Semantic Layer** to convert user queries into SQL, execute them, and return results with clear explanations.

The system is designed to be **accurate, safe, and interpretable**, mimicking a real-world AI data assistant.

---

## 🔥 Key Features

- 🧠 Natural Language → SQL conversion
- 🧩 Semantic Layer for business understanding
- 🔐 SQL validation (blocks unsafe queries)
- 🔄 Retry mechanism for failed queries
- 🗣️ Business-friendly query explanations
- 📊 Automatic execution on database
- ⚠️ Ambiguity detection (e.g., "top vendors")
- 📝 Logging for observability

---

## 🧠 Why Semantic Layer?

Naive text-to-SQL systems often fail due to lack of business context.

We introduced a **semantic layer** to:

- Define business metrics (e.g., revenue, outstanding)
- Map synonyms (e.g., "bills" → invoices)
- Provide table and column descriptions
- Guide correct JOIN relationships

This significantly improves query accuracy and reliability.

---

## 🏗️ Architecture
User Query
↓
Query Normalization
↓
Semantic Layer Injection
↓
LLM (SQL Generation)
↓
SQL Validator
↓
Query Executor
↓
Result + Explanation

---

## ⚙️ Tech Stack

- Python
- SQLite
- Groq (LLM inference)
- Pandas
- YAML (Semantic Layer)

---

## 📂 Project Structure
app/
├── main.py
├── engine/
│ ├── query_generator.py
│ ├── executor.py
│ ├── validator.py
│ ├── explainer.py
│
├── llm/
│ ├── llm_client.py
│ ├── prompt.py
│
├── semantic_loader.py
semantic_layer.yaml
data/
README.md
requirements.txt

---

## Key Highlights
- Built end-to-end NLP → SQL pipeline
- Implemented query validation to prevent unsafe SQL
- Handled ambiguous queries with clarification
- Integrated LLM with structured database execution
  
---

## 🧪 Example Queries

### Example 1

**User Query:**
What is our revenue?

**Generated SQL:**
```sql
SELECT SUM(grand_total)
FROM invoices
WHERE status = 'paid';
Explanation:
Uses invoices table
Filters only paid invoices
Calculates total revenue
Example 2
User Query:
Compare revenue of each vendor and show top 5
Generated SQL:
SELECT vendors.name, SUM(invoices.grand_total) AS revenue
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id
WHERE invoices.status = 'paid'
GROUP BY vendors.name
ORDER BY revenue DESC
LIMIT 5;
Explanation:
Counts total number of invoices in the database.