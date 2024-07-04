from pydantic import BaseModel
import yaml


def load_config(path: str, model: BaseModel) -> dict:
  with open(path, "r") as f:
    config = yaml.safe_load(f)

    _ = model(**config)
    return config
