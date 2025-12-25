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
    DEFAULT_THREAT = "Loki has stolen the Tesseract and is planning to open a portal to unleash an alien army upon New York City."
    DEFAULT_AVENGER1_NAME_FOR_SYNERGY = "Iron Man"
    DEFAULT_AVENGER2_NAME_FOR_SYNERGY = "Captain America"
    DEFAULT_AVENGER_NAME_FOR_WEAKNESS = "Hulk"

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

    def __build_prompt_for_rank_top_3_highest_stat(self, stat_name: str) -> str:
        from prompts.find_top_3_highest_stat import (
            build_find_top_3_highest_stat_prompt,
        )

        return build_find_top_3_highest_stat_prompt(self.raw_text, stat_name)

    def __build_prompt_for_composite_score(self) -> str:
        from prompts.calculate_composite_score import (
            build_calculate_composite_score_prompt,
        )

        return build_calculate_composite_score_prompt(self.raw_text)

    def __build_prompt_for_create_balanced_team(self, threat: str) -> str:
        from prompts.create_balanced_team import build_create_balanced_team_prompt

        return build_create_balanced_team_prompt(self.raw_text, threat)

    def __build_prompt_for_team_synergy_score(
        self, avenger1_name: str, avenger2_name: str
    ) -> str:
        from prompts.team_synergy_score import build_team_synergy_score_prompt

        return build_team_synergy_score_prompt(
            self.raw_text, avenger1_name, avenger2_name
        )

    def __build_prompt_for_weakness_assessment(self, avenger_name: str) -> str:
        from prompts.weakness_assessment import build_weakness_assessment_prompt

        return build_weakness_assessment_prompt(self.raw_text, avenger_name)

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

            case TaskTypes.CALCULATE_COMPOSITE_SCORE:
                avenger_name = kwargs.get(
                    "avenger_name", self.DEFAULT_AVENGER_NAME_FOR_ATTRIBUTES
                )
                return self.__build_prompt_for_composite_score()

            case TaskTypes.FIND_TOP_3_HIGHEST_STAT:
                stat = kwargs.get("stat", self.DEFAULT_STAT)
                return self.__build_prompt_for_rank_top_3_highest_stat(stat_name=stat)

            case TaskTypes.CREATE_BALANCED_TEAM:
                threat = kwargs.get("threat", self.DEFAULT_THREAT)
                return self.__build_prompt_for_create_balanced_team(threat)

            case TaskTypes.TEAM_SYNERGY_SCORE:
                avenger1_name = kwargs.get(
                    "avenger1_name", self.DEFAULT_AVENGER1_NAME_FOR_SYNERGY
                )
                avenger2_name = kwargs.get(
                    "avenger2_name", self.DEFAULT_AVENGER2_NAME_FOR_SYNERGY
                )
                return self.__build_prompt_for_team_synergy_score(
                    avenger1_name, avenger2_name
                )

            case TaskTypes.WEAKNESS_ASSESSMENT:
                avenger_name = kwargs.get(
                    "avenger_name", self.DEFAULT_AVENGER_NAME_FOR_WEAKNESS
                )
                return self.__build_prompt_for_weakness_assessment(avenger_name)

            case _:
                raise ValueError(f"Unsupported task type: {task_type}")
