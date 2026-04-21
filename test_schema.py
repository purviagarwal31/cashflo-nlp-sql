from app.semantic_loader import load_semantic_layer

schema = load_semantic_layer()
print(schema.keys())