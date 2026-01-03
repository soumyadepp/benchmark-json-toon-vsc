import logging
from dotenv import load_dotenv
from tasks import FileFormats, TaskTypes
from benchmarking import (
    BenchmarkingToolBase,
    BenchmarkingResultBase,
    BenchmarkingToolResultExporter,
    OpenAIBenchmarkingTool,
    OpenAIBenchmarkingReportExporter,
    GeminiBenchmarkingTool,
    GeminiBenchmarkingReportExporter,
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_benchmarking_on_file_format(
    tool_instance: BenchmarkingToolBase, file_format: FileFormats
) -> list[BenchmarkingResultBase]:
    """
    Runs a series of benchmarking tasks for a given tool instance and file format.

    This function executes a predefined set of benchmarking tasks using the provided
    tool instance. It iterates through various task types, such as calculating composite
    scores, assessing avenger capabilities, and creating balanced teams, all based on
    the specified file format.

    Args:
        tool_instance (BenchmarkingToolBase): An instance of a benchmarking tool (e.g.,
            OpenAIBenchmarkingTool, GeminiBenchmarkingTool) that will be used to run the
            tasks.
        file_format (FileFormats): The file format to be used for the input data during
            benchmarking. This determines which version of the dataset is used (e.g.,
            JSON, TOON, VSC).

    Returns:
        list[BenchmarkingResultBase]: A list of benchmarking result objects, where each
            object contains the results of a single benchmarking task.
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


def run_benchmarking_on_tool_and_export_results(
    tool: BenchmarkingToolBase,
    exporter: BenchmarkingToolResultExporter,
    filename: str = "benchmarking_results.csv",
) -> None:
    """
    Runs benchmarking tasks for a given tool across all file formats and exports the results.

    This function orchestrates the benchmarking process by iterating through all available
    file formats (JSON, TOON, VSC), running the full suite of benchmarking tasks for
    each, and then exporting the consolidated results to a CSV file.

    Args:
        tool (BenchmarkingToolBase): The benchmarking tool to be used (e.g.,
            OpenAIBenchmarkingTool, GeminiBenchmarkingTool).
        exporter (BenchmarkingToolResultExporter): The exporter to be used for saving
            the benchmarking results to a file.
        filename (str, optional): The name of the output CSV file. Defaults to
            "benchmarking_results.csv".
    """
    results: list[BenchmarkingResultBase] = []
    for file_format in FileFormats:
        results.extend(
            run_benchmarking_on_file_format(tool_instance=tool, file_format=file_format)
        )
    exporter.export_to_csv(results=results, filename=filename)


if __name__ == "__main__":
    # run_benchmarking_on_tool_and_export_results(
    #     tool=OpenAIBenchmarkingTool(),
    #     exporter=OpenAIBenchmarkingReportExporter(),
    #     filename="openai_benchmarking_results.csv",
    # )
    run_benchmarking_on_tool_and_export_results(
        tool=GeminiBenchmarkingTool(),
        exporter=GeminiBenchmarkingReportExporter(),
        filename="gemini_benchmarking_results.csv",
    )
