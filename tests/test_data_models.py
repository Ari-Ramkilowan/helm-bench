import pytest
from pydantic import ValidationError

from helm_bench.data_models import (
    Prompt,
    TextGenerationTask,
    ImageInformationExtractionTask,
    ModelConfig,
    BenchmarkResult,
)


def test_prompt_validation():
    # Valid
    p = Prompt(prompt_id="1", prompt_text="Hello")
    assert p.prompt_id == "1"
    assert p.prompt_text == "Hello"

    # Invalid
    with pytest.raises(ValidationError):
        Prompt(prompt_id="1")  # Missing prompt_text


def test_text_generation_task_validation():
    # Valid
    task = TextGenerationTask(
        task_id="1",
        task_type="text_generation",
        client_id="test_client",
        prompts=[Prompt(prompt_id="p1", prompt_text="test")],
    )
    assert task.task_type == "text_generation"

    # Invalid - wrong task_type
    with pytest.raises(ValidationError):
        TextGenerationTask(
            task_id="1",
            task_type="wrong_type",
            client_id="test_client",
            prompts=[],
        )


def test_image_information_extraction_task_validation(tmp_path):
    # Create a dummy image file
    image_file = tmp_path / "image.png"
    image_file.touch()

    # Valid
    task = ImageInformationExtractionTask(
        task_id="1",
        task_type="image_information_extraction",
        client_id="test_client",
        prompts=[Prompt(prompt_id="p1", prompt_text="test")],
        image_path=image_file,
    )
    assert task.image_path == image_file

    # Invalid - non-existent file
    with pytest.raises(ValidationError):
        ImageInformationExtractionTask(
            task_id="1",
            task_type="image_information_extraction",
            client_id="test_client",
            prompts=[],
            image_path="nonexistent.png",
        )


def test_model_config_validation():
    # Valid
    config = ModelConfig(model_id="gpt-4", provider="openai")
    assert config.model_id == "gpt-4"

    # Invalid
    with pytest.raises(ValidationError):
        ModelConfig(model_id="gpt-4")  # Missing provider


def test_benchmark_result_validation():
    # Valid
    result = BenchmarkResult(
        client_id="c1",
        task_id="t1",
        prompt_id="p1",
        model_id="m1",
        prompt_text="prompt",
        response="response",
    )
    assert result.model_id == "m1"

    # Invalid
    with pytest.raises(ValidationError):
        BenchmarkResult(client_id="c1", task_id="t1")  # Missing fields
