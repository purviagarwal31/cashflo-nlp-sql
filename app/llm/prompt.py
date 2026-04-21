def build_prompt(user_query, schema):
    return f"""
You are an expert SQL generator.

Convert the user question into a correct SQLite SQL query.

STRICT RULES:
- Only SELECT queries allowed
- Use ONLY tables and columns from the schema
- Use proper JOINs based on relationships
- Use aggregation when needed (SUM, COUNT, etc.)
- Do NOT hallucinate columns or tables
- Handle synonyms (e.g., bills = invoices, suppliers = vendors)
- Return ONLY SQL (no explanation, no markdown)

Examples:

Q: How many invoices are there?
A: SELECT COUNT(*) FROM invoices;

Q: List all vendors
A: SELECT * FROM vendors;

Q: Total revenue
A: SELECT SUM(grand_total) FROM invoices WHERE status = 'paid';

Schema:
{schema}

User Question:
{user_query}
"""