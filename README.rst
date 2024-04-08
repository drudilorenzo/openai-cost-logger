.. image:: https://img.shields.io/badge/chatGPT-74aa9c.svg?logo=openai
.. image:: https://img.shields.io/pypi/pyversions/setuptools.svg

==================
OpenAI Cost Logger
==================

Simple cost logger for OpenAI requests.
Track the cost of every request you make to OpenAI and visualize them in a user-friendly way.

How to install:
---------------
* .. code-block:: python

      pip install openai-cost-logger

* .. code-block:: python

      from openai_cost_logger.constants import DEFAULT_LOG_PATH, Models, MODELS_COST
      from openai_cost_logger.openai_cost_logger_viz import OpenAICostLoggerViz
      from openai_cost_logger.openai_cost_logger_utils import OpenAICostLoggerUtils
      from openai_cost_logger.openai_cost_logger import OpenAICostLogger

* See also the homepage on `PyPI <https://pypi.org/project/openai-cost-logger/>`_.
* See the `demo file <https://github.com/drudilorenzo/track-openai-cost/blob/master/demo.ipynb>`_ for a usage example.

Key Features:
-------------
* Track the cost of every request you make to OpenAI and save them in a csv file.
* Visualize the cost of all the requests you have made.

Endpoint supported:
-------------------
* Chat completion.
* Every endpoint which response contains the field "*usage.prompt_tokens*" and "*usage.completion_tokens*".
