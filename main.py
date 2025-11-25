import logging
from tasks import FileFormats, TaskTypes
from benchmarking import BenchmarkingToolBase
from benchmarking import OpenAIBenchmarkingTool
from benchmarking import GeminiBenchmarkingTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_benchmarking_on_tasks(tool: BenchmarkingToolBase) -> None:
    """Runs the provided benchmarking tool for all file formats
    for different tasks

    Args:
        tool (BenchmarkingToolBase): The benchmarking tool to use.
    """
    logger.info(f"Running benchmarking on {tool.__class__.__name__}")

    for file_format in FileFormats:
        tool.run_benchmarking_on_models(
            task_type=TaskTypes.CAN_AVENGER_HANDLE_THREAT,
            threat_description="There is a huge strong alien who can travel across dimensions",
            avenger_name="Doctor Strange",
            file_format=file_format,
        )
        tool.export_results_to_csv(
            f"{file_format.value}_{tool.__class__.__name__}_{TaskTypes.CAN_AVENGER_HANDLE_THREAT.value}_report.csv"
        )

        tool.run_benchmarking_on_models(
            task_type=TaskTypes.CAN_AVENGER_DEFEAT_AVENGER,
            avenger_1_name="Thor",
            avenger_2_name="Spiderman",
            file_format=file_format,
        )
        tool.export_results_to_csv(
            f"{file_format.value}_{tool.__class__.__name__}_{TaskTypes.CAN_AVENGER_DEFEAT_AVENGER.value}_report.csv"
        )

        tool.run_benchmarking_on_models(
            task_type=TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK,
            user_task="I want to break into a very secure building and steal important data",
            file_format=file_format,
        )
        tool.export_results_to_csv(
            f"{file_format.value}_{tool.__class__.__name__}_{TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK.value}_report.csv"
        )

        tool.run_benchmarking_on_models(
            task_type=TaskTypes.FIND_TOP_3_HIGHEST_STAT,
            stat="intelligence",
            file_format=file_format,
        )
        tool.export_results_to_csv(
            f"{file_format.value}_{tool.__class__.__name__}_{TaskTypes.FIND_TOP_3_HIGHEST_STAT.value}_report.csv"
        )

        tool.run_benchmarking_on_models(
            task_type=TaskTypes.CALCULATE_COMPOSITE_SCORE,
            file_format=file_format,
        )
        tool.export_results_to_csv(
            f"{file_format.value}_{tool.__class__.__name__}_{TaskTypes.CALCULATE_COMPOSITE_SCORE.value}_report.csv"
        )


if __name__ == "__main__":
    run_benchmarking_on_tasks(tool=OpenAIBenchmarkingTool())
    run_benchmarking_on_tasks(tool=GeminiBenchmarkingTool())
