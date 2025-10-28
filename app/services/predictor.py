from typing import Any, Dict, Optional


def predict(model: Optional[Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder prediction function.

    Replace with your model inference logic. Returns a simple dict so the
    controller and tests have a stable contract.
    """
    # If model is a dict (from loader placeholder), just echo input
    if model is None:
        return {"prediction": None, "confidence": 0.0, "notes": "no-model"}

    # Example dummy behavior: echo the processed data
    return {"prediction": data, "confidence": 1.0}
