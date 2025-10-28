import os
from typing import Any, Optional


def load_model(path: str) -> Optional[Any]:
    """Minimal model loader placeholder.

    Returns a simple object when the path exists. In production, load your
    ML artifact (torch, sklearn, etc.) and return the model object.
    """
    if os.path.exists(path):
        return {"model_path": path}
    return None
