import csv
import dataclasses
import logging
import os
import time
from typing import List
from google.generativeai.generative_models import GenerativeModel
from google.generativeai.client import configure

from tasks import FileFormats
from tasks import TaskTypes
from .prompt_builder import PromptBuilder
from .base import BenchmarkingToolBase, BenchMarkingResultBase
from .utils import calculate_latency

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class GeminiBenchmarkResult(BenchMarkingResultBase):
    pass


@dataclasses.dataclass
class GeminiBenchmarkingResults:
    """Container for a list of benchmark results."""

    results: list[GeminiBenchmarkResult]


class GeminiBenchmarkingTool(BenchmarkingToolBase):
    """A benchmarking tool for Gemini models."""

    MODELS_TO_ANALYZE: list[str] = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ]

    DIR_TO_SAVE_RESULTS: str = "reports/gemini/"

    def __init__(self) -> None:
        super().__init__()
        configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.results: GeminiBenchmarkingResults = GeminiBenchmarkingResults(results=[])

    def call_llm_and_format_response(
        self, model: str, prompt: str, task_type: TaskTypes, file_format: FileFormats
    ) -> GeminiBenchmarkResult | None:
        """Calls Gemini model with given prompt

        Args:
            model (str): The LLM model to use.
            prompt (str): The prompt to send to the model.


        Raises:
            ValueError: If the model is not supported.

        Returns:
            GenerateContentResponse: The response from the model.
        """
        if model not in self.MODELS_TO_ANALYZE:
            raise ValueError(f"Unsupported model: {model}")

        try:
            start_time = time.time()
            genai_model = GenerativeModel(model_name=model)
            response = genai_model.generate_content(
                prompt,
                generation_config={"temperature": 0.2},
                safety_settings=None,
            )
            return {
                "model": model,
                "file_format": file_format.name,
                "task_type": task_type.name,
                "latency_seconds": calculate_latency(start_time),
                "size_in_bytes": len(response.text.encode("utf-8")),
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count,
                "response": response.text,
            }
        except Exception as e:
            logger.error(f"Error calling Gemini model {model}: {e}")

    def run_benchmarking_on_models(
        self, task_type: TaskTypes, file_format: FileFormats, **kwargs
    ) -> None:
        """Run benchmarking on the MODELS_TO_ANALYZE.

        Args:
            task_type: The task for which benchmarking is to be run.
            file_format: The file format to use for the task.
            **kwargs: Additional keyword arguments.
        """
        bm_results: List[GeminiBenchmarkResult] = []

        logger.info(
            f"Prompting for task: {task_type.value} with file format: {file_format.name}"
        )
        try:
            prompt = PromptBuilder(file_format=file_format).build_prompt(
                task_type=task_type, **kwargs
            )
        except ValueError as e:
            logger.error("Unable to build prompt: %s", e)
            return

        try:
            for model in self.MODELS_TO_ANALYZE:
                logger.info(f"Using model: {model}")
                result = self.call_llm_and_format_response(
                    model=model,
                    prompt=prompt,
                    task_type=task_type,
                    file_format=file_format,
                )
                if result is None:
                    continue
                bm_results.append(result)
        except Exception as e:
            logger.error("Error running benchmarking: %s", e)
            return

        self.results = GeminiBenchmarkingResults(results=bm_results)

    def export_results_to_csv(self, file_path: str) -> None:
        """Exports the generated results to a CSV file.

        Args:
            file_path (str): The name of the file where the results are to be exported
        """
        benchmarking_results = self.results.results

        if not benchmarking_results:
            logger.warning("No results to export.")
            return

        keys = benchmarking_results[0].keys()
        file_path = os.path.join(self.DIR_TO_SAVE_RESULTS, file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(benchmarking_results)
            logger.info(f"Results exported to {file_path}")
