from groq import Groq
import os
from app.semantic_loader import load_semantic_layer
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
semantic = load_semantic_layer()


# =========================
# SQL GENERATION (UNCHANGED)
# =========================
def generate_sql(user_query):

    prompt = f"""
You are an expert SQL generator for a financial database.

Use this semantic layer:

Tables:
{semantic['tables']}

Relationships:
{semantic['relationships']}

Metrics:
{semantic['metrics']}

Synonyms:
{semantic.get('synonyms', {})}

Temporal Mappings:
{semantic.get('temporal', {})}

========================
IMPORTANT SCHEMA RULES
========================
- invoice_line_items:
  id, invoice_id, product_id, quantity, unit_rate, total_amount

- invoices:
  id, vendor_id, grand_total, status, created_at

- vendors:
  id, name

- products:
  id, name

========================
CRITICAL RULES
========================

NEVER:
- use unit_price
- guess column names

ALWAYS:
- use unit_rate or total_amount
- use SUM(invoice_line_items.total_amount) for product value
- use SUM(invoices.grand_total) for invoice value

- If query contains "previous":
    DO NOT use SUM anywhere

========================
JOINS
========================
- product → invoice_line_items JOIN products
- vendor → invoices JOIN vendors
- department → invoices → purchase_orders → departments

========================
WINDOW FUNCTIONS (STRICT)
========================

- Window functions must operate on row-level data

NEVER:
- GROUP BY with window functions
- LAG(SUM(...))
- SUM(SUM(...))

------------------------
RUNNING TOTAL
------------------------

Use EXACTLY:

SUM(invoices.grand_total) OVER (
    PARTITION BY invoices.vendor_id
    ORDER BY invoices.created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

------------------------
PREVIOUS VALUE
------------------------

Use EXACTLY:

LAG(invoices.grand_total) OVER (
    PARTITION BY invoices.vendor_id
    ORDER BY invoices.created_at
)

------------------------
WINDOW OUTPUT RULES
------------------------

ALWAYS include:
- entity name (vendors.name)
- created_at
- base column (invoices.grand_total)
- computed column

ALWAYS ORDER BY:
vendors.name, invoices.created_at

========================
RANKING (VERY IMPORTANT)
========================

- If query contains "rank":

    MUST use:

    RANK() OVER (ORDER BY metric DESC)

- When using RANK with aggregation:

    First aggregate using GROUP BY

Example:

SELECT 
  vendors.name,
  SUM(invoices.grand_total) AS total_value,
  RANK() OVER (ORDER BY SUM(invoices.grand_total) DESC) AS rank
FROM invoices
JOIN vendors ON invoices.vendor_id = vendors.id
GROUP BY vendors.name

========================
TEMPORAL RULES
========================

- "last month":
    created_at >= DATE('now','start of month','-1 month')
    AND created_at < DATE('now','start of month')

- "last quarter":
    created_at >= DATE('now','-3 months')

========================
AGGREGATION RULES
========================

- ALWAYS include:
    entity name + metric

- ALWAYS alias metrics:
    total_value, total_revenue

========================
TOP / HIGHEST
========================

- ORDER BY metric DESC
- LIMIT 5

========================
OUTPUT QUALITY
========================

- NEVER return only IDs
    - vendor_id
    - product_id

- ALWAYS return readable columns:
    vendors.name
    products.name

========================
BEST PRACTICES
========================

- ALWAYS partition using IDs (vendor_id), NOT names

- Prefer simple, correct SQL over complex SQL

========================
OUTPUT RULES
========================

- ONLY SQL
- NO explanation
- NO markdown

========================
User Query:
{user_query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


# =========================
# EXPLANATION GENERATION
# =========================
def generate_explanation(user_query, sql):
    prompt = f"""
You are a data analyst.

Explain how the SQL query answers the user's question.

Follow STRICT format:
- Tables used
- Joins performed
- Filters applied
- Aggregations or calculations

User Question:
{user_query}

SQL Query:
{sql}

Return ONLY bullet points.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    explanation = response.choices[0].message.content.strip()
    explanation = explanation.replace("```", "").strip()

    return explanation