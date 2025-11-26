import csv
import dataclasses
import os
import time
import logging


from typing import List
from openai import OpenAI

from .base import BenchmarkingToolBase, BenchMarkingResultBase
from .constants import COSTING_MAP
from .prompt_builder import PromptBuilder
from .utils import calculate_latency, calculate_cost
from tasks import TaskTypes, FileFormats

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class OpenAIBenchmarkResult(BenchMarkingResultBase):
    pass


@dataclasses.dataclass
class OpenAIBenchmarkingResults:
    """Container for a list of benchmark results."""

    results: List[OpenAIBenchmarkResult]


class OpenAIBenchmarkingTool(BenchmarkingToolBase):
    """A benchmarking tool for OpenAI models."""

    MODELS_TO_ANALYZE: list[str] = [
        "gpt-4o",
        "gpt-4",
        "gpt-5.1",
    ]

    DIR_TO_SAVE_RESULTS: str = "reports/openai/"

    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.results: OpenAIBenchmarkingResults = OpenAIBenchmarkingResults(results=[])

    def call_llm_and_format_response(
        self, model: str, prompt: str, task_type: TaskTypes, file_format: FileFormats
    ) -> OpenAIBenchmarkResult | None:
        """Calls the respective OpenAI model and returns the benchmarking response.

        Args:
            model (str): The name of the model to call.
            prompt (str): The prompt to use for the model.
            task_type (TaskTypes): The type of task to perform.
            file_format (FileFormats): The file format to use.

        Returns:
            OpenAIBenchmarkResult | None: The benchmarking response.
        """

        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            if (
                not response
                or not response.usage
                or not response.choices
                or not response.choices[0].message.content
            ):
                return None

            return {
                "model": model,
                "file_format": file_format.name,
                "task_type": task_type,
                "latency_seconds": calculate_latency(start_time),
                "size_in_bytes": len(
                    response.choices[0].message.content.encode("utf-8")
                ),
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "response": response.choices[0].message.content,
                "cost_in_usd": calculate_cost(
                    input_token_cost=COSTING_MAP[model]["input_token"],
                    output_token_cost=COSTING_MAP[model]["output_token"],
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                ),
            }
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")

    def run_benchmarking_on_models(
        self, task_type: TaskTypes, file_format: FileFormats, **kwargs
    ) -> None:
        """Run benchmarking on the models

        Args:
            task_type: The task for which benchmarking is to be run.
            **kwargs: Additional keyword arguments.
        """
        bm_results: List[OpenAIBenchmarkResult] = []

        logger.info(f"Prompting with file format: {file_format.name}")
        prompt = PromptBuilder(file_format=file_format).build_prompt(
            task_type=task_type, **kwargs
        )

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
        except Exception as e:
            logger.error("Error running benchmark %s", e)
            return

    def export_results_to_csv(self, file_path: str) -> None:
        """Export the benchmarking results DataFrame to a CSV file."""

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
