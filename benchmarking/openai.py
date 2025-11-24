import csv
import dataclasses
import os
import time
import logging


from typing import List
from openai import OpenAI

from .base import BenchmarkingToolBase, BenchMarkingResultBase
from .prompt_builder import PromptBuilder
from .utils import calculate_latency
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

    def run_benchmarking_on_models(self, task_type: TaskTypes, **kwargs) -> None:
        bm_results: List[OpenAIBenchmarkResult] = []

        for file_format in FileFormats:
            logger.info(f"Prompting with file format: {file_format.name}")
            prompt = PromptBuilder(file_format=file_format).build_prompt(
                task_type=task_type, **kwargs
            )

            for model in self.MODELS_TO_ANALYZE:
                logger.info(f"Using model: {model}")
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                )

                usage = response.usage
                response_content = response.choices[0].message.content

                if usage is None or response_content is None:
                    continue

                result: OpenAIBenchmarkResult = {
                    "model": model,
                    "file_format": file_format.name,
                    "task_type": task_type,
                    "latency_seconds": calculate_latency(start_time),
                    "size_in_bytes": len(response_content.encode("utf-8")),
                    "prompt_tokens": usage.prompt_tokens or 0,
                    "completion_tokens": usage.completion_tokens or 0,
                    "total_tokens": usage.total_tokens or 0,
                    "response": response_content,
                }
                bm_results.append(result)

        self.results = OpenAIBenchmarkingResults(results=bm_results)

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
