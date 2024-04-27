import os
import json
from typing import Dict
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

from openai_cost_logger.constants import DEFAULT_LOG_PATH


"""Cost logger visualizer."""
class OpenAICostLoggerViz:
    
    @staticmethod
    def get_total_cost(path: str = DEFAULT_LOG_PATH) -> float:
        """Return the total cost of all the logs in the directory.

        Args:
            log_folder (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                        This method reads all the files in the specified directory.
        Returns:
            float: the total cost.
        """
        cost = 0
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(Path(path, filename), mode='r') as file:
                    data = json.load(file)
                    cost += data["total_cost"]
        return cost
    
    
    @staticmethod
    def print_total_cost(path: str = DEFAULT_LOG_PATH) -> None:
        """Print the total cost of all the logs in the directory.

        Args:
            log_folder (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                        This method reads all the files in the specified directory.
        """
        print(f"Total cost: {round(OpenAICostLoggerViz.get_total_cost(path), 6)} (USD)")
    
    
    @staticmethod
    def get_total_cost_by_model(path: str = DEFAULT_LOG_PATH) -> Dict[str, float]:
        """Return the total cost by model of all the logs in the directory.

        Args:
            log_folder (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                        This method reads all the files in the specified directory.

        Returns:
            Dict[str, float]: the total cost by model.
        """
        cost_by_model = defaultdict(float)
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(Path(path, filename), mode='r') as file:
                    data = json.load(file)
                    for entry in data["breakdown"]:
                        cost_by_model[entry["model"]] += entry["cost"]
        return cost_by_model


    def print_total_cost_by_model(path: str = DEFAULT_LOG_PATH) -> None:
        """Print the total cost by model of all the logs in the directory.

        Args:
            log_folder (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                        This method reads all the files in the specified directory.
        """
        cost_by_model = OpenAICostLoggerViz.get_total_cost_by_model(path=path)
        for model, cost in cost_by_model.items():
            print(f"{model}: {round(cost, 6)} (USD)")


    @staticmethod
    def plot_cost_by_strftime(path: str = DEFAULT_LOG_PATH, strftime_aggregator: str = "%Y-%m-%d", last_n_days: int = None) -> None:
        """Plot the cost by day of all the logs in the directory aggregated using strftime_aggregator.

        Args:
            path (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                  This method reads all the files in the specified directory.
            last_n_days (int, optional): The number of last days to plot. Defaults to None.
        """
        cost_by_aggregation_key = defaultdict(float)
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(Path(path, filename), mode='r') as file:
                    data = json.load(file)
                    creation_datetime = datetime.strptime(data["creation_datetime"], "%Y-%m-%d %H:%M:%S")
                    aggregation_key = creation_datetime.strftime(strftime_aggregator)
                    cost_by_aggregation_key[aggregation_key] += data["total_cost"]
        
        cost_by_aggregation_key = dict(sorted(cost_by_aggregation_key.items(), key=lambda x: x[0]))
        if last_n_days:
            cost_by_aggregation_key = dict(list(cost_by_aggregation_key.items())[-last_n_days:])
        
        plt.bar(cost_by_aggregation_key.keys(), cost_by_aggregation_key.values(), width=0.5)
        plt.xticks(rotation=30, fontsize=8)
        plt.xlabel('Day')
        plt.ylabel('Cost [$]')
        plt.title('Cost by day')
        plt.tight_layout()
        plt.show()
        
        
    @staticmethod
    def plot_cost_by_day(path: str = DEFAULT_LOG_PATH, last_n_days: int = None) -> None:
        """Plot the cost by day of all the logs in the directory.

        Args:
            path (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                  This method reads all the files in the specified directory.
            last_n_days (int, optional): The number of last days to plot. Defaults to None.
        """
        OpenAICostLoggerViz.plot_cost_by_strftime(
            path=path,
            strftime_aggregator="%Y-%m-%d", 
            last_n_days=last_n_days
        )