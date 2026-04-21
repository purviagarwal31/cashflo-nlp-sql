from groq import Groq
import os
from app.semantic_loader import load_semantic_layer
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
semantic = load_semantic_layer()

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

Instructions:
- Use proper joins based on relationships
- Map synonyms (e.g., bills = invoices)
- Use metrics when relevant (e.g., revenue)
- Return ONLY SQL, no explanation

User Query:
{user_query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()