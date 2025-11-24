import textwrap

CAN_AVENGER_DEFEAT_AVENGER = textwrap.dedent(
    """
    You are an expert analyst tasked with determining if one Avenger can defeat another in a hypothetical battle.
    You are given a dataset of Avengers below. The dataset may appear in any structure, order, or style.
    Your job:
    1. Read and understand the given data exactly as it is.
    2. Assess whether the first specified Avenger has the capabilities to defeat the second specified Avenger based on the attributes visible in the data.
    3. Explain your reasoning strictly based on the data provided.
    4. Do not invent powers, descriptions, or Avengers that are not present.
    5. If either of the provided Avengers is not found in the data, state that clearly.
    
    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---
    
    Avenger 1:
    {avenger_1_name}
    
    Avenger 2:
    {avenger_2_name}
    
    Provide your answer in the following format:
    Can Defeat: <Yes/No/Unknown>
    Reason: <brief explanation>
"""
)


def build_can_avenger_defeat_avenger_prompt(
    raw_text: str, avenger_1_name: str, avenger_2_name: str
) -> str:
    return CAN_AVENGER_DEFEAT_AVENGER.format(
        raw_text=raw_text,
        avenger_1_name=avenger_1_name,
        avenger_2_name=avenger_2_name,
    )
