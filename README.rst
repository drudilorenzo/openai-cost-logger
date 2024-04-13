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
* Track the cost of every request you make and save them in a JSON file.
* Choose the feature you want to track (prompt_tokens, completion_tokens, completion, prompt, etc.).
* Check the cost of your requests filtering by model or strftime aggregation (see the docs).

Endpoint supported:
-------------------
* Chat completion.
* Every response passed to *OpenAICostLogger* should contain the fields "*usage.prompt_tokens*" and "*usage.completion_tokens*".
  This is the only strict requirement of the library, the way you call the OpenAI API is totally up to you. If needed, you can
  find an easy example in the demo file.

Viz examples:
-------------
.. image::images/viz_prints.png
   :alt: Viz prints examples.
   :align: center
   :width: 500px

.. image::images/strftime_agg.png
   :alt: Strftime aggregation example.
   :align: center
   :width: 500px   

