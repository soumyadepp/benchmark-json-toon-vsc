import textwrap

FIND_TOP_3_HIGHEST_STAT = textwrap.dedent(
    """
You are an expert analyst tasked with ranking the avengers according
to the highest value of the provided stat. The dataset may appear in any
structure, order or style.

Your job:
1. Read and understand the given data exactly as it is.
2. List the top 3 avengers based on the provided stat. If it's a tie,
use speed as the tie breaker.
3. Explain your reasoning strictly based on the data provided.
4. Do not invent powers, descriptions, or Avengers that are not present.

--- BEGIN AVENGERS DATA ---
{raw_text}
--- END AVENGERS DATA ---

Stat to Assess:
{stat}

Provide your answer in the following format:

Ranked avengers:
<name1>
<name2>
<name3>
Reason: <brief explanation>
"""
)


def build_find_top_3_highest_stat_prompt(raw_text: str, stat: str) -> str:
    """
    Builds a prompt for finding the top 3 Avengers with the highest stat.

    This function constructs a prompt that instructs a language model to act as an
    expert analyst and rank the top three Avengers based on a specified stat.
    The prompt includes the raw text of the Avengers dataset and the stat to be
    assessed.

    Args:
        raw_text (str): The raw text of the Avengers dataset.
        stat (str): The stat to be used for ranking (e.g., "intelligence", "strength").

    Returns:
        str: A formatted prompt ready to be used with a language model.
    """
    return FIND_TOP_3_HIGHEST_STAT.format(raw_text=raw_text, stat=stat)
