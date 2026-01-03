import textwrap

TEAM_SYNERGY_SCORE = textwrap.dedent(
    """
    You are a strategic analyst responsible for evaluating the synergy between Avengers.

    You are given a dataset of Avengers below. The dataset may appear in any
    structure, order, or style. DO NOT attempt to reformat it. DO NOT assume missing
    information. Only rely on what is explicitly present in the data.

    Your job:

    1. Read and understand the given data exactly as it is.
    2. Analyze the provided pair of Avengers.
    3. Calculate a "synergy score" out of 100 for the pair.
    4. The synergy score should reflect how well their powers, stats, and abilities complement each other.
       For example, a high-tech character might have good synergy with another high-tech or high-intelligence character.
       A character with high attack but low defense might pair well with a character with high defense.
    5. Provide a short reason for your score, explaining the basis for your assessment.
    6. Do not invent powers, descriptions, or Avengers that are not present.

    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---

    Avenger Pair:
    - {avenger1_name}
    - {avenger2_name}

    Provide your answer in the following format:

    Synergy Score: <score>/100
    Reason: <Brief explanation of the synergy and how the score was determined>
"""
)


def build_team_synergy_score_prompt(
    raw_text: str, avenger1_name: str, avenger2_name: str
) -> str:
    """
    Builds a prompt for calculating the synergy score between two Avengers.

    This function constructs a prompt that instructs a language model to act as a
    strategic analyst and evaluate the synergy between a pair of Avengers. The
    prompt includes the raw text of the Avengers dataset and the names of the two
    Avengers to be assessed.

    Args:
        raw_text (str): The raw text of the Avengers dataset.
        avenger1_name (str): The name of the first Avenger in the pair.
        avenger2_name (str): The name of the second Avenger in the pair.

    Returns:
        str: A formatted prompt ready to be used with a language model.
    """
    return TEAM_SYNERGY_SCORE.format(
        raw_text=raw_text, avenger1_name=avenger1_name, avenger2_name=avenger2_name
    )
