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
    AVENGER_OVERALL_ATTRIBUTES = "avenger_overall_attributes"
    ASSESS_RESPONSE_CONSISTENCY = "assess_response_consistency"
    CHOOSE_AVENGER_WITH_HIGHEST_STAT = "choose_avenger_with_highest_stat"
