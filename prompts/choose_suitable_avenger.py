import textwrap

CHOOSE_SUITABLE_AVENGER = textwrap.dedent(
    """
    You are an expert selector responsible for choosing the most suitable Avenger
    to help a user with a specific task.

    You are given a dataset of Avengers below. The dataset may appear in any 
    structure, order, or style. DO NOT attempt to reformat it. DO NOT assume missing 
    information. Only rely on what is explicitly present in the data.

    Your job:

    1. Read and understand the given data exactly as it is.
    2. Identify which Avenger best matches the user's need.
    3. Explain the reasoning based strictly on the attributes visible in the data.
    4. Do not invent powers, descriptions, or Avengers that are not present.

    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---

    User Task:
    {user_task}

    Provide your answer in the following format:

    Chosen Avenger: <name>
    Reason: <brief explanation>
"""
)


def build_suitable_avenger_prompt(raw_text: str, user_task: str) -> str:
    """
    Builds a prompt for choosing a suitable Avenger for a given task.

    This function constructs a prompt that instructs a language model to act as an
    expert selector and choose the most suitable Avenger to help a user with a
    specific task. The prompt includes the raw text of the Avengers dataset and the
    user's task description.

    Args:
        raw_text (str): The raw text of the Avengers dataset.
        user_task (str): The task the user wants to accomplish.

    Returns:
        str: A formatted prompt ready to be used with a language model.
    """
    return CHOOSE_SUITABLE_AVENGER.format(raw_text=raw_text, user_task=user_task)
