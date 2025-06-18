from pydantic import BaseModel


class PredictRequest(BaseModel):
    instances: list[str] | None = None


class PredictResponse(BaseModel):
    model_id: str
    predictions: list[int]


class PredictDemoResponse(PredictResponse):
    source_demo_image_base64: str | None = None
