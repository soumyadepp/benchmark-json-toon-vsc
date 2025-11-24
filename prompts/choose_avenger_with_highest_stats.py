import textwrap

CHOOSE_AVENGER_WITH_HIGHEST_STAT = textwrap.dedent(
    """
    You are an expert analyst tasked with finding the avenger with
    the highest value of the provided stat. The dataset may appear in any
    structure, order or style.
    
    Your job:
    1. Read and understand the given data exactly as it is.
    2. Find the avenger who has the highest value of the specified stat.
    3. Explain your reasoning strictly based on the data provided.
    4. Do not invent powers, descriptions, or Avengers that are not present.
    
    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---
    
    Stat to Assess:
    {stat}
    
    Provide your answer in the following format:
    Avenger with Highest {stat}: <name>
    Reason: <brief explanation>
    """
)


def build_choose_avenger_with_highest_stat_prompt(raw_text: str, stat: str) -> str:
    return CHOOSE_AVENGER_WITH_HIGHEST_STAT.format(raw_text=raw_text, stat=stat)
