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
from .constants import COSTING_MAP
from .prompt_builder import PromptBuilder
from .base import (
    BenchmarkingToolBase,
    BenchmarkingResultBase,
    BenchmarkingToolResultExporter,
)
from .utils import calculate_latency, calculate_cost

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class GeminiBenchmarkResult(BenchmarkingResultBase):
    """Represents the result of a single benchmark run using a Gemini model."""

    pass


@dataclasses.dataclass
class GeminiBenchmarkingResults:
    """
    A container class for storing a list of Gemini benchmark results.

    This class is used to group together the results of multiple benchmarking runs,
    making it easier to manage and process the data collectively.
    """

    results: list[GeminiBenchmarkResult]


class GeminiBenchmarkingTool(BenchmarkingToolBase):
    """A benchmarking tool for Gemini models."""

    MODELS_TO_ANALYZE: list[str] = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
    ]

    DIR_TO_SAVE_RESULTS: str = "reports/gemini/"

    def __init__(self) -> None:
        super().__init__()
        configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.results: GeminiBenchmarkingResults = GeminiBenchmarkingResults(results=[])

    def call_llm_and_format_response(
        self,
        model: str,
        prompt: str,
        task_type: TaskTypes,
        file_format: FileFormats,
    ) -> GeminiBenchmarkResult | None:
        """
        Calls the Gemini model with the given prompt and formats the response.

        This method sends a prompt to the specified Gemini model, measures the
        performance of the call, and formats the response into a structured
        `GeminiBenchmarkResult` object. It captures metrics such as latency, token
        counts, and cost.

        Args:

            model (str): The name of the Gemini model to use (e.g., "gemini-2.0-flash").

            prompt (str): The prompt to send to the model.

            task_type (TaskTypes): The type of task being benchmarked.

            file_format (FileFormats): The file format used for the input data.

        Raises:

            ValueError: If the specified model is not supported by this tool.

        Returns:
            GeminiBenchmarkResult | None: A `GeminiBenchmarkResult` object containing
                the benchmarking data, or `None` if an error occurred during the API
                call.
        """

        if model not in self.MODELS_TO_ANALYZE:
            raise ValueError(f"Unsupported model: {model}")

        try:
            start_time = time.time()
            genai_model = GenerativeModel(model_name=model)
            response = genai_model.generate_content(
                prompt,
                generation_config={"temperature": 0},
                safety_settings=None,
            )
            return {
                "model": model,
                "file_format": file_format.name,
                "task_type": task_type,
                "latency_seconds": calculate_latency(start_time),
                "size_in_bytes": len(response.text.encode("utf-8")),
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count,
                "response": response.text,
                "cost_in_usd": calculate_cost(
                    input_token_cost=COSTING_MAP[model]["input_token"],
                    output_token_cost=COSTING_MAP[model]["output_token"],
                    input_tokens=response.usage_metadata.prompt_token_count,
                    output_tokens=response.usage_metadata.candidates_token_count,
                ),
            }
        except Exception as e:
            logger.error(f"Error calling Gemini model {model}: {e}")

    def run_benchmarking_on_models(
        self, task_type: TaskTypes, file_format: FileFormats, **kwargs
    ) -> list[GeminiBenchmarkResult]:
        """
        Runs benchmarking for a given task and file format across all supported models.

        This method builds a prompt for the specified task, then iterates through the
        list of supported Gemini models, calling each one with the prompt. It collects
        the results of each model execution and returns them as a list.

        Args:
            task_type (TaskTypes): The type of task to benchmark.
            file_format (FileFormats): The file format to use for the task's input data.
            **kwargs: Additional keyword arguments to be passed to the prompt builder.

        Returns:
            list[GeminiBenchmarkResult]: A list of `GeminiBenchmarkResult` objects,
                with each object representing the result of a single model's execution.
                Returns an empty list if an error occurs.
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
            return []

        try:
            for model in self.MODELS_TO_ANALYZE:
                logger.info(f"Using model: {model}")
                result = self.call_llm_and_format_response(
                    model=model,
                    prompt=prompt,
                    task_type=task_type,
                    file_format=file_format,
                )
                if not result:
                    continue

                bm_results.append(result)

            return bm_results
        except Exception as e:
            logger.error("Error running benchmarking: %s", e)
            return []


class GeminiBenchmarkingReportExporter(BenchmarkingToolResultExporter):
    """
    A class for exporting Gemini benchmarking results to a CSV file.

    This class provides the functionality to take a list of Gemini benchmark
    results and write them to a specified CSV file, making it easy to save and
    analyze the data.
    """

    def __init__(self) -> None:
        self.DIR_TO_SAVE_RESULTS = "reports/gemini"

    def export_to_csv(
        self, results: list[GeminiBenchmarkResult], filename: str
    ) -> None:
        """Exports the generated results for gemini models to a CSV file.

        Args:
            results (list[GeminiBenchmarkResult]): The list of rows to be exported.
            filename (str): The name of the file where the results are to be exported.
        """

        if not results:
            logger.warning("No results to export.")
            return

        keys = results[0].keys()
        file_path = os.path.join(self.DIR_TO_SAVE_RESULTS, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
            logger.info(f"Results exported to {file_path}")
