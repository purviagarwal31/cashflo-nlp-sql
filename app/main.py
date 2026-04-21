from app.engine.query_generator import generate_query
from app.engine.executor import execute_query
from app.engine.validator import validate_sql
from app.engine.explainer import explain_query


def run():
    print("✅ System Ready! Ask your question (type 'exit' to quit)\n")

    while True:
        user_query = normalize_query(input("Ask your question: "))

        if user_query.lower() == "exit":
            print("👋 Exiting...")
            break

        # 🔥 Smart Ambiguity Handling
        uq = user_query.lower()
        if "top vendors" in uq and "revenue" not in uq and "invoice" not in uq:
            print("⚠️ Do you mean top vendors by revenue or by invoice count?\n")
            continue

        try:
            # 🧠 Generate SQL
            sql = generate_query(user_query)
            print("\n🧠 Generated SQL:\n", sql)

            # ✅ Validate SQL (with user intent)
            is_valid, message = validate_sql(sql, user_query)
            if not is_valid:
                print("\n❌ Validation Error:", message)
                continue

            # 📊 Execute Query
            result = execute_query(sql)

            # 🔁 Retry if execution fails
            if isinstance(result, str):
                print("\n❌ Execution Error:", result)
                print("⚠️ Retrying with improved query...\n")

                sql = generate_query(user_query)
                print("\n🧠 Regenerated SQL:\n", sql)

                result = execute_query(sql)

            print("\n📊 Result:\n", result)

            # 🧾 Explanation
            explanation = explain_query(user_query, sql)
            print("\n🧾 Explanation:\n", explanation)

            # 📝 Logging
            with open("logs.txt", "a") as f:
                f.write("\n" + "=" * 50 + "\n")
                f.write(f"User Query: {user_query}\n")
                f.write(f"SQL: {sql}\n")
                f.write(f"Result: {str(result)}\n")
                f.write(f"Explanation: {explanation}\n")

            print("\n" + "-" * 50)

        except Exception as e:
            print("\n❌ Error:", str(e))

def normalize_query(query):
    query = query.lower()
    query = query.replace("bills", "invoices")
    query = query.replace("suppliers", "vendors")
    return query

if __name__ == "__main__":
    run()