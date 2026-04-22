from app.engine.query_generator import generate_query
from app.engine.executor import execute_query
from app.engine.validator import validate_sql


# Auto-fix common LLM mistakes
def fix_sql(sql: str) -> str:
    fixes = {
        "unit_price": "unit_rate",
        "price": "unit_rate"
    }

    for wrong, correct in fixes.items():
        sql = sql.replace(wrong, correct)

    return sql


# Normalize query
def normalize_query(query):
    query = query.lower()

    replacements = {
        "bills": "invoices",
        "suppliers": "vendors",
        "products": "product",
        "items": "product",
        "revenue": "total paid invoices",
        "top": "highest"
    }

    for k, v in replacements.items():
        query = query.replace(k, v)

    return query


# Chart suggestion
def suggest_chart(query):
    if "trend" in query or "over time" in query or "running" in query:
        return "Line Chart"
    elif "distribution" in query or "share" in query:
        return "Pie Chart"
    else:
        return "Bar Chart"


#  Interpretation + SQL explanation
def explain(user_query, sql):
    explanation = []

    query = user_query.lower()
    sql_lower = sql.lower()

    # Interpretation Layer (NEW)
    if "unpaid" in query:
        explanation.append("Interpreted 'unpaid' as invoices not marked as paid")

    if "revenue" in query:
        explanation.append("Interpreted 'revenue' as sum of paid invoice amounts")

    if "top" in query or "highest" in query:
        explanation.append("Interpreted 'top' as highest total value")

    if "last month" in query:
        explanation.append("Interpreted 'last month' using date filters on created_at")

    if "last quarter" in query:
        explanation.append("Interpreted 'last quarter' using past 3 months filter")

    if "previous" in query:
        explanation.append("Interpreted 'previous' using LAG window function")

    if "running" in query:
        explanation.append("Interpreted 'running total' using cumulative SUM over time")

    # SQL Breakdown
    if "from invoices" in sql_lower:
        explanation.append("Used invoices table")

    if "join vendors" in sql_lower:
        explanation.append("Joined with vendors to fetch vendor names")

    if "join products" in sql_lower:
        explanation.append("Joined with products for product details")

    if "where" in sql_lower:
        explanation.append("Applied filters based on conditions")

    if "status = 'paid'" in sql_lower:
        explanation.append("Filtered only paid invoices")

    if "sum(" in sql_lower:
        explanation.append("Calculated total using SUM aggregation")

    if "count(" in sql_lower:
        explanation.append("Counted total number of records")

    if "group by" in sql_lower:
        explanation.append("Grouped results by relevant entity")

    if "rank()" in sql_lower:
        explanation.append("Ranked results using window function")

    if "over (" in sql_lower:
        explanation.append("Used window function for advanced calculation")

    # fallback
    if not explanation:
        explanation.append("Generated SQL based on user query interpretation")

    return "\n- " + "\n- ".join(explanation)


def run():
    print("System Ready! Ask your question (type 'exit' to quit)\n")

    while True:
        user_input = input("Ask your question: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        user_query = normalize_query(user_input)
        print("\nNormalized Query:", user_query)

        # Ambiguity handling
        if "vendor" in user_query and "highest" in user_query:
            if "revenue" not in user_query and "invoice" not in user_query:
                print("Assuming 'top vendors' means by total invoice value\n")

        if "product" in user_query and "price" in user_query:
            print("Assuming 'price' means unit_rate\n")

        try:
            # Generate SQL
            sql = generate_query(user_query)
            sql = fix_sql(sql)

            print("\nGenerated SQL:\n", sql)

            # Validate
            is_valid, message = validate_sql(sql, user_query)
            if not is_valid:
                print("\nValidation Error:", message)
                continue

            # Execute
            result = execute_query(sql)

            # Retry if needed
            if isinstance(result, str):
                error_msg = result

                print("\nExecution Error:", error_msg)
                print("Retrying...\n")

                improved_query = f"""
User Query:
{user_query}

Previous SQL:
{sql}

Error:
{error_msg}

Fix the SQL.
"""

                sql = generate_query(improved_query)
                sql = fix_sql(sql)

                print("\nRegenerated SQL:\n", sql)

                result = execute_query(sql)

                if isinstance(result, str):
                    print("\nRetry Failed:", result)
                    continue

            # TEMPORAL FALLBACK
            if hasattr(result, "empty") and result.empty and "last month" in user_query:
                print("\nNo data found for last month — showing all invoices instead\n")

                fallback_sql = "SELECT * FROM invoices LIMIT 10"
                result = execute_query(fallback_sql)

            # Output
            print("\nResult:\n", result)

            # Chart
            chart = suggest_chart(user_query)
            print(f"\nSuggested Chart: {chart}")

            # Explanation
            explanation = explain(user_query, sql)
            print("\nExplanation:", explanation)

            print("\n" + "-" * 50)

        except Exception as e:
            print("\nError:", str(e))


if __name__ == "__main__":
    run()
