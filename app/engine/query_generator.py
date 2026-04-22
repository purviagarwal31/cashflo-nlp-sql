from app.semantic_loader import load_semantic_layer
from app.llm.prompt import build_prompt
from app.llm.llm_client import generate_sql


def generate_query(user_query):
    schema = load_semantic_layer()   # single source of truth
    
    prompt = build_prompt(user_query, schema)
    sql = generate_sql(prompt)
    
    return sql