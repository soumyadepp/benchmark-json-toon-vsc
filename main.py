import logging
from tasks import TaskTypes
from benchmarking import BenchmarkingToolBase
from benchmarking import OpenAIBenchmarkingTool
from benchmarking import GeminiBenchmarkingTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_benchmarking_on_tasks(tool: BenchmarkingToolBase) -> None:
    tool.run_benchmarking_on_models(
        task_type=TaskTypes.CAN_AVENGER_HANDLE_THREAT,
        threat_description="There is a huge strong alien who can travel across dimensions",
        avenger_name="Doctor Strange",
    )
    tool.export_results_to_csv(
        f"{tool.__class__.__name__}_{TaskTypes.CAN_AVENGER_HANDLE_THREAT.value}_report.csv"
    )

    tool.run_benchmarking_on_models(
        task_type=TaskTypes.CAN_AVENGER_DEFEAT_AVENGER,
        avenger_1_name="Thor",
        avenger_2_name="Spiderman",
    )
    tool.export_results_to_csv(
        f"{tool.__class__.__name__}_{TaskTypes.CAN_AVENGER_DEFEAT_AVENGER.value}_report.csv"
    )

    tool.run_benchmarking_on_models(
        task_type=TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK,
        user_task="I want to break into a very secure building and steal important data",
    )
    tool.export_results_to_csv(
        f"{tool.__class__.__name__}_{TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK.value}_report.csv"
    )

    tool.run_benchmarking_on_models(
        task_type=TaskTypes.CHOOSE_AVENGER_WITH_HIGHEST_STAT,
        stat="intelligence",
    )
    tool.export_results_to_csv(
        f"{tool.__class__.__name__}_{TaskTypes.CHOOSE_AVENGER_WITH_HIGHEST_STAT.value}_report.csv"
    )


if __name__ == "__main__":
    run_benchmarking_on_tasks(tool=OpenAIBenchmarkingTool())
    run_benchmarking_on_tasks(tool=GeminiBenchmarkingTool())
