def validate_sql(sql, user_query):
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    # ❌ Block dangerous SQL
    for word in forbidden:
        if word in sql.upper():
            return False, "Unsafe query detected"

    # ❌ Only allow SELECT
    if "SELECT" not in sql.upper():
        return False, "Only SELECT queries allowed"

    # 🔥 Intent-based validation
    if "delete" in user_query.lower():
        return False, "User intent is destructive. Query blocked."

    return True, "Valid SQL"