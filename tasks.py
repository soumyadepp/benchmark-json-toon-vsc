from enum import Enum


class FileFormats(str, Enum):
    """The file formats that we will be benchmarking"""

    JSON = "json"
    TOON = "toon"
    VSC = "vsc"


class TaskTypes(str, Enum):
    """
    All supported tasks that the LLMs can perform
    """

    FIND_SUITABLE_AVENGER_FOR_TASK = "find_suitable_avenger"
    CAN_AVENGER_HANDLE_THREAT = "can_avenger_handle_threat"
    CAN_AVENGER_DEFEAT_AVENGER = "can_avenger_defeat_avenger"
    CALCULATE_COMPOSITE_SCORE = "calculate_composite_score"
    FIND_TOP_3_HIGHEST_STAT = "find_top_3_highest_stat"
    ASSESS_RESPONSE_CONSISTENCY = "assess_response_consistency"
    CREATE_BALANCED_TEAM = "create_balanced_team"
    TEAM_SYNERGY_SCORE = "team_synergy_score"
    WEAKNESS_ASSESSMENT = "weakness_assessment"
