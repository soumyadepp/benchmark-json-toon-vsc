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

    def run_benchmarking_on_models(self, task_type: TaskTypes, **kwargs) -> None:
        """Run benchmarking on the MODELS_TO_ANALYZE.

        Args:
            task_type: The task for which benchmarking is to be run.
            **kwargs: Additional keyword arguments.
        """
        bm_results: List[GeminiBenchmarkResult] = []

        for file_format in FileFormats:
            logger.info(f"Prompting with file format: {file_format.name}")
            prompt = PromptBuilder(file_format=file_format).build_prompt(
                task_type=task_type, **kwargs
            )

            for model in self.MODELS_TO_ANALYZE:
                logger.info(f"Using model: {model}")
                start_time = time.time()
                genai_model = GenerativeModel(model_name=model)

                response = genai_model.generate_content(
                    prompt, generation_config={"temperature": 0.2}, safety_settings=None
                )
                text = response.text or ""
                usage = response.usage_metadata
                input_tokens = usage.prompt_token_count or 0
                output_tokens = usage.candidates_token_count or 0
                total_tokens = input_tokens + output_tokens

                result: GeminiBenchmarkResult = {
                    "model": model,
                    "file_format": file_format.value,
                    "task_type": task_type.name,
                    "latency_seconds": calculate_latency(start_time),
                    "size_in_bytes": len(text.encode("utf-8")),
                    "prompt_tokens": input_tokens or 0,
                    "completion_tokens": output_tokens or 0,
                    "total_tokens": total_tokens or 0,
                    "response": text,
                }
                bm_results.append(result)

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
