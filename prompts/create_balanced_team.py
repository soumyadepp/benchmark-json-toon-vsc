import textwrap

CREATE_BALANCED_TEAM = textwrap.dedent(
    """
    You are a strategic expert responsible for assembling a balanced team of Avengers
    to handle a specific threat.

    You are given a dataset of Avengers below. The dataset may appear in any 
    structure, order, or style. DO NOT attempt to reformat it. DO NOT assume missing 
    information. Only rely on what is explicitly present in the data.

    Your job:

    1. Read and understand the given data exactly as it is.
    2. Analyze the given threat.
    3. Select a balanced team of 3 Avengers with complementary skills to counter the threat.
    4. Provide a justification for your team composition, explaining how the chosen Avengers' skills
       and stats work together to address the threat.
    5. Do not invent powers, descriptions, or Avengers that are not present.

    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---

    Threat:
    {threat}

    Provide your answer in the following format:

    Chosen Team:
    - <Avenger 1 Name>
    - <Avenger 2 Name>
    - <Avenger 3 Name>

    Justification: <Detailed explanation of why this team is balanced and effective against the threat>
"""
)


def build_create_balanced_team_prompt(raw_text: str, threat: str) -> str:
    return CREATE_BALANCED_TEAM.format(raw_text=raw_text, threat=threat)
