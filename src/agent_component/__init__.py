from src.utils import load_config

config = load_config('config.yaml')

TOOL_MODELS = config['tools']
LLM_MODELS = config['llm']
TOP_K = config["astradb"]["top_k"]