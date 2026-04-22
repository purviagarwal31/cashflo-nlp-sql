# NLP-to-SQL System with Semantic Layer

### *(Cashflo Hiring Challenge – Problem B)*

---

## Problem Chosen

**Problem B: Semantic Layer on a Database for NLP-to-Query Conversion**

---

## Overview

This project builds an **AI-powered data analyst system** that allows users to query a financial database using natural language.

Instead of directly converting text → SQL, the system introduces a **Semantic Layer** to bridge the gap between business language and database schema.

### Example

> **User Query:** “Show me unpaid bills”
> **Interpretation:** invoices where status is not paid

---

## What the System Does

* Converts natural language → SQL
* Executes SQL on database
* Returns:

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

### Includes:

* **Table & Column Descriptions**
* **Relationships (JOIN paths)**
* **Business Metrics**

  * `revenue = SUM(grand_total WHERE status = 'paid')`
* **Synonyms**

  * bills → invoices
  * suppliers → vendors
* **Temporal Expressions**

  * last month
  * last quarter

This significantly improves SQL accuracy over naive text-to-SQL systems.

---

## Features

* Natural Language → SQL conversion
* Semantic-aware query generation
* SQL validation (blocks DELETE/DROP/UPDATE)
* Prevents unsafe queries and enforces schema correctness
* Retry mechanism for failed queries
* Ambiguity handling (assumptions for vague queries)
* Interpretation-based explanations
* Chart suggestions (Bar / Line / Pie)
* Logging for observability

---

## NLP → SQL Pipeline (Detailed)

1. **User Query Input**
2. **Normalization Layer**

   * Converts synonyms (e.g., "bills" → invoices)
3. **Semantic Injection**

   * Injects schema, relationships, metrics, temporal rules
4. **LLM SQL Generation**

   * Generates structured SQL using strict prompting
5. **Validation Layer**

   * Blocks unsafe or incorrect SQL
6. **Execution Engine**

   * Runs query on SQLite database
7. **Post-processing**

   * Explanation generation
   * Chart suggestion

---

## How Interpretation Works

For each query, the system:

* Identifies intent (aggregation, ranking, filtering)
* Resolves synonyms using semantic layer (e.g., "bills" → invoices)
* Applies business logic (e.g., revenue = paid invoices)
* Maps temporal expressions (e.g., last month)
* Generates SQL accordingly

### Example

**User:** Show unpaid bills

**Interpretation:**

* Entity → invoices
* Filter → status != 'paid'
* Output → full invoice records

---

## AI Tools Used

This project was developed using AI-assisted workflows:

### ChatGPT

* Prompt engineering
* Debugging and system design
* Iterated prompts multiple times for accuracy

### Groq (LLM: llama-3.3-70b-versatile)

* SQL generation
* Explanation generation

AI tools were used as **development accelerators**, not replacements for system design.

---

## Tradeoffs & Limitations

* Temporal queries depend on dataset availability (may return empty results)
* Explanation layer is rule-based + LLM-assisted (can be improved further)
* CLI-based system (no UI)
* No query caching or multi-turn conversations
* Some interpretations (e.g., “unpaid”) depend on dataset-specific status values

---

## How to Run

```bash
git clone <your-repo-link>
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
Built end-to-end NLP → SQL pipeline
Introduced semantic layer for business understanding
Implemented SQL validation & retry mechanism
Supported advanced SQL (window functions, ranking)
Focused on interpretability and correctness
Demo

https://www.loom.com/share/102e697384b44444b4f2f59b6d3304cb

Sample Queries & Outputs
1. Simple Query

Input:

How many invoices are there?

SQL:

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
7. Ambiguity Handling

Input:

Top vendors

System Behavior:

Assuming "top vendors" means by total invoice value

SQL:

SELECT vendors.name, SUM(invoices.grand_total) AS total_value
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id
GROUP BY vendors.name
ORDER BY total_value DESC
LIMIT 5;
Future Improvements
Multi-turn conversational queries
Query caching and reuse
UI dashboard for visualization
Schema auto-discovery
Conclusion

This project demonstrates how combining LLMs with a semantic layer enables accurate, explainable, and production-ready natural language querying over structured databases.

Unlike naive text-to-SQL systems, this approach:

Reduces hallucinations using structured semantic context
Improves join accuracy and metric correctness

It moves toward building a real-world AI data assistant.