# NLP-to-SQL System with Semantic Layer (Cashflo Hiring Challenge – Problem B)

## Problem Chosen

**Problem B: Semantic Layer on a Database for NLP-to-Query Conversion**

---

## Overview

This project builds an **AI-powered data analyst system** that allows users to query a financial database using natural language.

Instead of directly converting text → SQL, the system introduces a **Semantic Layer** to bridge the gap between business language and database schema.

Example:

> “Show me unpaid bills”
> → correctly interpreted as
> → invoices where status is not paid

The system generates SQL, validates it, executes it on a database, and returns:

* Query results
* Human-readable explanation
* Visualization suggestion

---

## System Architecture


User Query
↓
Query Normalization
↓
Semantic Layer (Context Injection)
↓
LLM (Groq - SQL Generation)
↓
SQL Validation Layer
↓
Query Execution (SQLite)
↓
Result + Explanation + Chart Suggestion


---

## Semantic Layer (Core Innovation)

The semantic layer provides **business context** to the LLM.

It includes:

* Table & Column Descriptions
* Relationships (JOIN paths)
* Business Metrics

  * revenue = SUM(grand_total WHERE status = 'paid')
* Synonyms

  * bills → invoices
  * suppliers → vendors
* Temporal Expressions

  * last month
  * last quarter

This improves SQL accuracy compared to naive text-to-SQL systems.

---

## Features

* Natural Language → SQL conversion
* Semantic-aware query generation
* SQL validation (blocks unsafe queries like DELETE/DROP)
* Retry mechanism for failed SQL
* Ambiguity handling (asks or assumes intent)
* Business-friendly explanations
* Chart suggestions (bar / line / pie)
* Logging for debugging and traceability

---

AI Tools Used

This project was developed using AI-assisted workflows:

ChatGPT
Used for prompt engineering, debugging, and system design decisions
Iterated prompts multiple times for better SQL accuracy
Groq (LLM - llama-3.3-70b-versatile)
Used for SQL generation and explanation

AI tools were used as development accelerators, not replacements for system design.

Tradeoffs & Limitations
Temporal queries depend on dataset availability (may return empty results)
Explanation layer is rule-based + LLM-assisted (can be improved further)
No UI (CLI-based system)
No query caching or multi-turn conversations (future scope)
Some interpretations (e.g., "unpaid") depend on dataset-specific status values and may require semantic tuning
How to Run
git clone <repo>
cd project
pip install -r requirements.txt

python -m app.main
Project Structure
app/
├── main.py
├── engine/
│   ├── query_generator.py
│   ├── executor.py
│   ├── validator.py
│
├── llm/
│   ├── llm_client.py
│
├── semantic_loader.py

semantic_layer.yaml
data/
README.md
requirements.txt
Key Highlights
Built a semantic-aware NLP-to-SQL system
Designed modular architecture
Implemented query validation & retry logic
Supported advanced SQL (window functions, ranking)
Focused on interpretability and correctness

Demo

https://www.loom.com/share/102e697384b44444b4f2f59b6d3304cb

---

## Future Improvements
- Multi-turn conversations
- Query caching
- UI dashboard

---


## Sample Queries & Outputs

### 1. Simple Query

**Input:**


How many invoices are there?


**SQL:**

```sql
SELECT COUNT(*) FROM invoices;
2. Synonym Handling

Input:

Show me all unpaid bills

SQL:

SELECT * FROM invoices WHERE status != 'paid';
3. Join Query

Input:

Show invoices with vendor names

SQL:

SELECT invoices.id, vendors.name, invoices.grand_total
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id;
4. Aggregation

Input:

What is total revenue?

SQL:

SELECT SUM(grand_total)
FROM invoices
WHERE status = 'paid';
5. Window Function (Advanced)

Input:

Show running total of invoices for each vendor

SQL:

SELECT 
  vendors.name,
  invoices.created_at,
  SUM(invoices.grand_total) OVER (
    PARTITION BY invoices.vendor_id
    ORDER BY invoices.created_at
  ) AS running_total
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id;
6. Ranking

Input:

Rank vendors by total invoice value

SQL:

SELECT 
  vendors.name,
  SUM(invoices.grand_total) AS total_value,
  RANK() OVER (ORDER BY SUM(invoices.grand_total) DESC) AS rank
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id
GROUP BY vendors.name;

Conclusion

This project demonstrates how combining LLMs with a semantic layer enables accurate, explainable, and production-ready natural language querying over structured databases.