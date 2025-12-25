import textwrap

WEAKNESS_ASSESSMENT = textwrap.dedent(
    """
    You are a strategic analyst specializing in identifying vulnerabilities.

    You are given a dataset of Avengers below. The dataset may appear in any
    structure, order, or style. DO NOT attempt to reformat it. DO NOT assume missing
    information. Only rely on what is explicitly present in the data.

    Your job:

    1. Read and understand the given data exactly as it is.
    2. Analyze the specified Avenger.
    3. Identify potential weaknesses based on their stats and description. For example, a low 'tech' 
       stat might be a vulnerability in scenarios requiring technological interaction, or a purely
       physical hero might be vulnerable to psionic attacks.
    4. Provide a brief explanation for each identified weakness.
    5. Do not invent powers, descriptions, or Avengers that are not present.

    --- BEGIN AVENGERS DATA ---
    {raw_text}
    --- END AVENGERS DATA ---

    Avenger to Assess:
    {avenger_name}

    Provide your answer in the following format:

    Potential Weaknesses:
    - <Weakness 1>: <Brief explanation>
    - <Weakness 2>: <Brief explanation>
"""
)


def build_weakness_assessment_prompt(raw_text: str, avenger_name: str) -> str:
    return WEAKNESS_ASSESSMENT.format(raw_text=raw_text, avenger_name=avenger_name)
