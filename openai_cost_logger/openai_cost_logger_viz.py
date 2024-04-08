import os
import csv
from typing import Dict
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict

from openai_cost_logger.constants import DEFAULT_LOG_PATH

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
            with open(Path(path, filename), mode='r') as file:
                csvreader = csv.reader(file)
                next(csvreader)
                for row in csvreader:
                    cost += float(row[2])
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
            with open(Path(path, filename), mode='r') as file:
                csvreader = csv.reader(file)
                next(csvreader)
                for row in csvreader:
                    if row[1] not in cost_by_model:
                        cost_by_model[row[1]] = 0
                    cost_by_model[row[1]] += float(row[2])
        return cost_by_model
    
    def print_total_cost_by_model(path: str = DEFAULT_LOG_PATH) -> None:
        """Print the total cost by model of all the logs in the directory.

        Args:
            log_folder (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                        This method reads all the files in the specified directory.
        """
        cost_by_model = OpenAICostLoggerViz.get_total_cost_by_model(path)
        for model, cost in cost_by_model.items():
            print(f"{model}: {round(cost, 6)} (USD)")
        
    @staticmethod
    def plot_cost_by_day(path: str = DEFAULT_LOG_PATH, last_n_days: int = None) -> None:
        """Plot the cost by day of all the logs in the directory.

        Args:
            path (str, optional): Cost logs directory. Defaults to DEFAULT_LOG_PATH.
                                  This method reads all the files in the specified directory.
            last_n_days (int, optional): The number of last days to plot. Defaults to None.
        """
        cost_by_day = defaultdict(float)
        for filename in os.listdir(path):
            with open(Path(path, filename), mode='r') as file:
                csvreader = csv.reader(file)
                next(csvreader)
                for row in csvreader:
                    day = filename.split("_")[2]
                    cost_by_day[day] += float(row[2])
        
        cost_by_day = dict(sorted(cost_by_day.items(), key=lambda x: x[0]))
        if last_n_days:
            cost_by_day = dict(list(cost_by_day.items())[-last_n_days:])
        
        plt.bar(cost_by_day.keys(), cost_by_day.values(), width=0.5)
        plt.xlabel('Day')
        plt.ylabel('Cost [$]')
        plt.title('Cost by day')
        plt.show()