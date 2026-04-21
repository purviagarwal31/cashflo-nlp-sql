import yaml

def load_semantic_layer(path="semantic_layer.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)