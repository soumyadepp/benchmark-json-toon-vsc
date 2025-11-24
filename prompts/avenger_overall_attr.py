import textwrap

AVENGER_OVERALL_ATTR_SCORE = textwrap.dedent(
    """
    You are an expert analyst tasked with summarizing the overall attributes of a specific Avenger.
    You are given a dataset of Avengers below. The dataset may appear in any structure, order, or style.
    Your job:
    1. Read and understand the given data exactly as it is.
    2. Summarize and calculate an overall attribute score for the specified Avenger based on the attributes visible in the data.
    3. Explain your reasoning strictly based on the data provided.
    4. Do not invent powers, descriptions, or Avengers that are not present.
    5. If the provided Avenger is not found in the data, state that clearly
    
    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---
    
    Avenger to Summarize:
    {avenger_name}
    
    Provide your answer in the following format:
    Overall Attribute Score: <score out of 100>
    Reason: <brief explanation>
"""
)


def build_avenger_overall_attr_prompt(raw_text: str, avenger_name: str) -> str:
    return AVENGER_OVERALL_ATTR_SCORE.format(
        raw_text=raw_text,
        avenger_name=avenger_name,
    )
