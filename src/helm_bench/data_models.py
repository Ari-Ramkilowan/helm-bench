from pydantic import BaseModel, FilePath
from typing import Literal, List


class Prompt(BaseModel):
    prompt_id: str
    prompt_text: str


class TextGenerationTask(BaseModel):
    task_id: str
    task_type: Literal["text_generation"]
    client_id: str
    prompts: List[Prompt]


class ImageInformationExtractionTask(BaseModel):
    task_id: str
    task_type: Literal["image_information_extraction"]
    client_id: str
    prompts: List[Prompt]
    image_path: FilePath


class ModelConfig(BaseModel):
    model_id: str
    provider: str
    # Future fields: api_key, endpoint, etc.


class BenchmarkResult(BaseModel):
    client_id: str
    task_id: str
    prompt_id: str
    model_id: str
    prompt_text: str
    response: str
    # Future fields: cost, latency, etc.
