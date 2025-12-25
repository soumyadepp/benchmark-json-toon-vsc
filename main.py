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
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.CREATE_BALANCED_TEAM,
            file_format=file_format,
            threat="Loki has stolen the Tesseract and is planning to open a portal to unleash an alien army upon New York City.",
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.TEAM_SYNERGY_SCORE,
            file_format=file_format,
            avenger1_name="Iron Man",
            avenger2_name="Captain America",
        )
    )
    results.extend(
        tool_instance.run_benchmarking_on_models(
            task_type=TaskTypes.WEAKNESS_ASSESSMENT,
            file_format=file_format,
            avenger_name="Hulk",
        )
    )

    return results


def run_benchmarking_on_tool_and_export_results(tool: BenchmarkingToolBase):
    results: list[BenchmarkingResultBase] = []
    for file_format in FileFormats:
        results.extend(
            run_benchmarking_on_file_format(tool_instance=tool, file_format=file_format)
        )
    if isinstance(tool, OpenAIBenchmarkingTool):
        exporter = OpenAIBenchmarkingReportExporter()
        exporter.export_to_csv(results=results, filename="tasks-openai.csv")
    elif isinstance(tool, GeminiBenchmarkingTool):
        exporter = GeminiBenchmarkingReportExporter()
        exporter.export_to_csv(results=results, filename="tasks-gemini.csv")


if __name__ == "__main__":
    run_benchmarking_on_tool_and_export_results(tool=OpenAIBenchmarkingTool())
