import yaml

with open("app/semantic_layer/schema.yaml", "r") as f:
    schema = yaml.safe_load(f)

print(schema.keys())