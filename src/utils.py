import yaml

def load_config(file_path):
    """Load a YAML configuration file and return its contents as a dictionary."""
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def merge_dicts(a:dict, b:dict):
    """
    Merge two dictionaries into one.

    Args:
        a (dict): The first dictionary.
        b (dict): The second dictionary.

    Returns:
        dict: A new dictionary containing all items from both input dictionaries.
        If the second dictionary is empty, returns the second dictionary.
    """

    if b == {}:
        return b
    else:
        return {**a, **b}

def result_template(result:dict)->tuple[str,str]:
    """
    Creates a formatted string from a dictionary of agent results.

    Args:
        result (dict): A dictionary of agent results, where the keys are the agent names and the values are the results.

    Returns:
        tuple[str,str]: A tuple where the first item is a string of the agent names, comma-separated, and the second item is the formatted string of the results.
    """
    content = "\n\n".join(
        f"**{agent}**:\n{content}"
        for agent, content in result.items()
    )
    agents = ", ".join(result.keys())
    return agents, content