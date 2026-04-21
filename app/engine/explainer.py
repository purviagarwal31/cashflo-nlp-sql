from app.llm.llm_client import generate_sql

def explain_query(user_query, sql):
    prompt = f"""
Explain in simple English what this SQL query is doing.

User Question: {user_query}
SQL Query: {sql}
"""

    explanation = generate_sql(prompt)
    return explanation