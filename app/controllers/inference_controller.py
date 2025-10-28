from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, Optional

from app.services.predictor import predict
from app.services.preprocessor import preprocess
from app.utils.loader import load_model

router = APIRouter()


class PredictRequest(BaseModel):
    data: Dict[str, Any]


@router.post("/predict")
def predict_endpoint(req: PredictRequest):
    """Simple inference endpoint that runs preprocess -> load_model -> predict.

    This is a minimal placeholder implementation. Replace the loader and
    predictor implementations with actual model code.
    """
    processed = preprocess(req.data)
    model = load_model("app/models/model.pt")
    result = predict(model, processed)
    return {"result": result}
