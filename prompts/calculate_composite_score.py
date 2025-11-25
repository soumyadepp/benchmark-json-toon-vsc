import textwrap

CALCULATE_COMPOSITE_SCORE = textwrap.dedent(
    """
    You are an expert analyst tasked with calculating the composite
    score of each avenger in the list. The composite score is defined as:
    
    score = attack*0.3 + defence*0.25 + speed*0.2 + intelligence*0.15 + tech*0.1
    
    Your job:
    1. Read and understand the given data exactly as it is.
    2. Find and display the composite score for each Avenger.
    3. Explain your reasoning strictly based on the data provided.
    4. Do not invent powers, descriptions, or Avengers that are not present.
    
    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---
    
    Provide your answer in the following format:
    <avenger_1_name>: <composite_score_of_avenger_1>
    Reasoning: <brief explanation>
    <avenger_2_name>: <composite_score_of_avenger_2>
    Reasoning: <brief explanation>
    ...
    <avenger_n_name>: <composite_score_of_avenger_n>
    Reasoning: <brief explanation>
    """
)


def build_calculate_composite_score_prompt(raw_text: str) -> str:
    return CALCULATE_COMPOSITE_SCORE.format(raw_text=raw_text)
