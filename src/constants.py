from enum import Enum

"""Default value for the cost-logs directory."""
DEFAULT_LOG_PATH = "cost-logs"

"""Enum containing the tested models."""
class Models(Enum):
    TURBO_3_5 = "gpt-3.5-turbo"
    TURBO_3_5_INSTRUCT = "gpt-3.5-turbo-instruct"
    AZURE_3_5_TURBO = "gpt-35-turbo-0125"
    AZURE_4_TURBO = "gpt-4-0125-Preview"
    AZURE_4 = "gpt-4-0613"

"""The costs of the models above (per million tokens)."""
MODELS_COST = {
    "gpt-3.5-turbo": {
        "input": 0.5,
        "output": 1.5
    },
    "gpt-35-turbo-0125": {
        "input": 0.5,
        "output": 1.5
    },
    "gpt-3.5-turbo-instruct": {
        "input": 1.5,
        "output": 2
    },
    "gpt-4-0125-Preview": {
        "input": 10,
        "output": 30
    },
    "gpt-4-0613": {
        "input": 30,
        "output": 60
    },
}