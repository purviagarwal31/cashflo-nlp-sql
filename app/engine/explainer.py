from app.llm.llm_client import generate_sql

def explain_query(user_query, sql):
    prompt = f"""
You are an expert data analyst.

Explain the SQL query in simple business-friendly English.

Follow this format strictly:
- Tables used
- Filters applied
- Aggregations (if any)
- Final output

User Question:
{user_query}

SQL Query:
{sql}

Return ONLY explanation in bullet points.
"""

    explanation = generate_sql(prompt)
    return explanation.strip()