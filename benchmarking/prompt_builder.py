from tasks import TaskTypes, FileFormats
from .utils import read_raw


class PromptBuilder:
    """A class to build prompts for different tasks and file formats."""

    DEFAULT_USER_TASK = "I need help with a high-stakes technological problem that requires innovative solutions."
    DEFAULT_THREAT_DESCRIPTION = (
        "A massive cyber attack which threatens global security."
    )
    DEFAULT_AVENGER_1_NAME = "Iron Man"
    DEFAULT_AVENGER_2_NAME = "Captain America"
    DEFAULT_AVENGER_NAME_FOR_THREAT = "Thor"
    DEFAULT_AVENGER_NAME_FOR_ATTRIBUTES = "Doctor Strange"
    DEFAULT_STAT = "attack"

    def __init__(self, file_format: FileFormats) -> None:
        self.file_format = file_format
        self.raw_text = read_raw(f"input-files/raw-data.{file_format.value}")

    def __build_prompt_for_finding_suitable_avenger_for_task(
        self, user_task: str
    ) -> str:
        from prompts.choose_suitable_avenger import build_suitable_avenger_prompt

        return build_suitable_avenger_prompt(self.raw_text, user_task)

    def __build_prompt_for_can_avenger_handle_threat(
        self, threat_description: str, avenger_name: str
    ) -> str:
        from prompts.can_avenger_handle_threat import (
            build_can_avenger_handle_threat_prompt,
        )

        return build_can_avenger_handle_threat_prompt(
            self.raw_text, threat_description, avenger_name
        )

    def __build_prompt_for_can_avenger_defeat_avenger(
        self, avenger_1_name: str, avenger_2_name: str
    ) -> str:
        from prompts.can_avenger_defeat_avenger import (
            build_can_avenger_defeat_avenger_prompt,
        )

        return build_can_avenger_defeat_avenger_prompt(
            self.raw_text, avenger_1_name, avenger_2_name
        )

    def __build_prompt_for_avenger_overall_attributes(self, avenger_name: str) -> str:
        from prompts.avenger_overall_attr import (
            build_avenger_overall_attr_prompt,
        )

        return build_avenger_overall_attr_prompt(self.raw_text, avenger_name)

    def __build_prompt_for_avenger_with_highest_stat(self, stat_name: str) -> str:
        from prompts.choose_avenger_with_highest_stats import (
            build_choose_avenger_with_highest_stat_prompt,
        )

        return build_choose_avenger_with_highest_stat_prompt(self.raw_text, stat_name)

    def build_prompt(self, task_type: TaskTypes, **kwargs) -> str:
        """Build a prompt based on the task type and file format.

        Args:
            task (TaskTypes): The type of task to build the prompt for.
            file_format (FileFormats): The file format of the input data.
        Raises:
            ValueError: If the task type is unsupported.
        Returns:
            str: The constructed prompt.
        """
        match task_type:
            case TaskTypes.FIND_SUITABLE_AVENGER_FOR_TASK:
                user_task = kwargs.get(
                    "user_task",
                    self.DEFAULT_USER_TASK,
                )
                return self.__build_prompt_for_finding_suitable_avenger_for_task(
                    user_task
                )

            case TaskTypes.CAN_AVENGER_HANDLE_THREAT:
                threat_description = kwargs.get(
                    "threat_description", self.DEFAULT_THREAT_DESCRIPTION
                )
                avenger_name = kwargs.get(
                    "avenger_name", self.DEFAULT_AVENGER_NAME_FOR_THREAT
                )
                return self.__build_prompt_for_can_avenger_handle_threat(
                    threat_description, avenger_name
                )

            case TaskTypes.CAN_AVENGER_DEFEAT_AVENGER:
                avenger_1_name = kwargs.get(
                    "avenger_1_name", self.DEFAULT_AVENGER_1_NAME
                )
                avenger_2_name = kwargs.get(
                    "avenger_2_name", self.DEFAULT_AVENGER_2_NAME
                )
                return self.__build_prompt_for_can_avenger_defeat_avenger(
                    avenger_1_name, avenger_2_name
                )

            case TaskTypes.AVENGER_OVERALL_ATTRIBUTES:
                avenger_name = kwargs.get(
                    "avenger_name", self.DEFAULT_AVENGER_NAME_FOR_ATTRIBUTES
                )
                return self.__build_prompt_for_avenger_overall_attributes(avenger_name)

            case TaskTypes.CHOOSE_AVENGER_WITH_HIGHEST_STAT:
                stat = kwargs.get("stat", self.DEFAULT_STAT)
                return self.__build_prompt_for_avenger_with_highest_stat(stat_name=stat)

            case _:
                raise ValueError(f"Unsupported task type: {task_type}")
