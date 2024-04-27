"""Default value for the cost-logs directory."""
DEFAULT_LOG_PATH = "cost-logs"
    

"""The costs of the models above (per million tokens). Dictionary used in case the user does not provide the costs."""
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
    "text-embedding-ada-002": {
        "input": 0.1,
        "output": 0.0
    }
}