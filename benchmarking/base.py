import abc
import dataclasses
from typing import TypedDict
from tasks import TaskTypes


@dataclasses.dataclass
class BenchMarkingResultBase(TypedDict):
    """A base class for benchmarking results."""

    model: str
    file_format: str
    task_type: str
    latency_seconds: float
    size_in_bytes: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response: str


class BenchmarkingToolBase(abc.ABC):
    """A base class for all benchmarking tools."""

    @abc.abstractmethod
    def run_benchmarking_on_models(self, task_type: TaskTypes, **kwargs) -> None:
        """Run benchmarking on a list of models for a given task.

        Args:
            task_type: The type of task to benchmark.
            **kwargs: Additional keyword arguments to pass to the prompt builder.
        """
        pass

    @abc.abstractmethod
    def export_results_to_csv(self, file_path: str) -> None:
        """Export the benchmarking results to a CSV file.

        Args:
            file_path: The path to the CSV file to export the results to.
        """
        pass
