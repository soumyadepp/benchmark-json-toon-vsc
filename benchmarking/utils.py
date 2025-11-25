import time


def read_raw(path: str) -> str:
    """Reads raw text from a file.

    Args:
        path (str): The file path to read from.

    Returns:
        str: The content of the file as a string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def calculate_latency(start_time: float) -> float:
    """Calculate the latency given a start time.

    Args:
        start_time (float): The start time in seconds.

    Returns:
        float: The latency in seconds.
    """
    return time.time() - start_time


def calculate_cost(
    input_token_cost: float,
    output_token_cost: float,
    input_tokens: int,
    output_tokens: int,
    round_off_digits: int = 5,
) -> float:
    """Calculates the cost of the prompt execution from the given input_token_cost,
    output_token_cost, input_tokens and output_tokens.

    Args:
        input_token_cost: Cost per input token in USD ($)
        output_token_cost: Cost per output token in USD ($)
        input_tokens: The number of tokens in the prompt
        output_tokens: The number of tokens in the response

    Returns:
        float: The total cost of the prompt execution
    """
    return round(
        input_token_cost * input_tokens + output_token_cost * output_tokens,
        round_off_digits,
    )
