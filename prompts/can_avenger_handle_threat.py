import textwrap

CAN_AVENGER_HANDLE_THREAT = textwrap.dedent(
    """
    You are an expert analyst tasked with determining if a specific Avenger can handle a given threat.
    You are given a dataset of Avengers below. The dataset may appear in any structure, order, or style.
    
    Your job:
    1. Read and understand the given data exactly as it is.
    2. Assess whether the specified Avenger has the capabilities to handle the described threat based on the attributes visible in the data.
    3. Explain your reasoning strictly based on the data provided.
    4. Do not invent powers, descriptions, or Avengers that are not present.
    5. If the provided Avenger is not found in the data, state that clearly.
    6. If the threat description is missing or unclear, indicate that as well.
    
    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---
    
    Threat Description:
    {threat_description}
    
    Avenger to Assess:
    {avenger_name}
    
    Provide your answer in the following format:
    Can Handle Threat: <Yes/No/Unknown>
    Reason: <brief explanation>
"""
)


def build_can_avenger_handle_threat_prompt(
    raw_text: str, threat_description: str, avenger_name: str
) -> str:
    """
    Builds a prompt for determining if an Avenger can handle a given threat.

    This function constructs a prompt that instructs a language model to act as an
    expert analyst and assess whether a specified Avenger has the capabilities to
    handle a described threat. The prompt includes the raw text of the Avengers
    dataset, the threat description, and the name of the Avenger to be assessed.

    Args:
        raw_text (str): The raw text of the Avengers dataset.
        threat_description (str): A description of the threat to be handled.
        avenger_name (str): The name of the Avenger to assess.

    Returns:
        str: A formatted prompt ready to be used with a language model.
    """
    return CAN_AVENGER_HANDLE_THREAT.format(
        raw_text=raw_text,
        threat_description=threat_description,
        avenger_name=avenger_name,
    )
