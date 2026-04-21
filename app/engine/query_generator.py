import yaml
from app.llm.prompt import build_prompt
from app.llm.llm_client import generate_sql

def load_schema():
    with open("app/semantic_layer/schema.yaml", "r") as f:
        return yaml.safe_load(f)

def generate_query(user_query):
    schema = load_schema()
    prompt = build_prompt(user_query, schema)
    
    sql = generate_sql(prompt)
    
    return sql