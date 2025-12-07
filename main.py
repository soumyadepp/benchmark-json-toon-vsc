import logging
from tasks import FileFormats, TaskTypes
from benchmarking import (
    BenchmarkingToolBase,
    BenchmarkingResultBase,
    OpenAIBenchmarkResult,
    GeminiBenchmarkResult,
    OpenAIBenchmarkingTool,
    OpenAIBenchmarkingReportExporter,
    GeminiBenchmarkingTool,
    GeminiBenchmarkingReportExporter,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_benchmarking_on_file_format(
    tool_instance: BenchmarkingToolBase, file_format: FileFormats
) -> list[BenchmarkingResultBase]:
    """Runs benchmarking for all tasks on all models of a given benchmarker for a single file format.

    Args:
        file_format (FileFormats): The file format to take input in.
    """
    results: list[BenchmarkingResultBase] = []
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.CALCULATE_COMPOSITE_SCORE, file_format=file_format
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.CAN_AVENGER_DEFEAT_AVENGER,
            file_format=file_format,
            avenger_1_name="Thor",
            avenger_2_name="Spiderman",
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.CAN_AVENGER_HANDLE_THREAT,
            file_format=file_format,
            threat_description="There is an attack to all data centers in the world, breaching global security.",
            avenger_name="Captain America",
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.FIND_TOP_3_HIGHEST_STAT,
            file_format=file_format,
            stat_name="intelligence",
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK,
            file_format=file_format,
            user_task="I want to explore multi dimensional reality and learn mystic arts",
        )
    )

    return results


if __name__ == "__main__":
    openai_results: list[OpenAIBenchmarkResult] = []
    gemini_results: list[GeminiBenchmarkResult] = []
    for file_format in FileFormats:
        openai_results.extend(
            run_benchmarking_on_file_format(OpenAIBenchmarkingTool(), file_format)
        )
        gemini_results.extend(
            run_benchmarking_on_file_format(GeminiBenchmarkingTool(), file_format)
        )

    openai_results_exporter = OpenAIBenchmarkingReportExporter()
    gemini_results_exporter = GeminiBenchmarkingReportExporter()
    openai_results_exporter.export_to_csv(
        results=openai_results, filename="tasks-openai.csv"
    )
    gemini_results_exporter.export_to_csv(
        results=gemini_results, filename="tasks-gemini.csv"
    )
