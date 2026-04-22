from app.llm.llm_client import generate_sql

def explain_query(user_query, sql):
    sql_lower = sql.lower()
    explanation = []

    # Tables
    if "join" in sql_lower:
        explanation.append("• Multiple tables are joined to combine related data")

    # Filters
    if "where" in sql_lower:
        explanation.append("• Filters are applied to narrow down results")

    # Aggregations
    if "sum(" in sql_lower:
        explanation.append("• Aggregation: summing values")
    if "count(" in sql_lower:
        explanation.append("• Aggregation: counting records")

    # Grouping
    if "group by" in sql_lower:
        explanation.append("• Results are grouped by a category")

    # Sorting
    if "order by" in sql_lower:
        explanation.append("• Results are sorted")

    # Limit
    if "limit" in sql_lower:
        explanation.append("• Only top results are returned")

    if not explanation:
        explanation.append("• Basic query without complex transformations")

    return "\n".join(explanation)