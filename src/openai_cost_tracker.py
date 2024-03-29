import csv
from enum import Enum
from pathlib import Path
from time import strftime
from typing import List, Dict
from openai import OpenAI, AzureOpenAI

from constants import DEFAULT_LOG_PATH

"""Clients supported."""
class ClientType(Enum):
    OPENAI = 1,
    AZURE = 2

"""Every cost is per million tokens."""
COST_UNIT = 1_000_000

"""Header of the cost log file."""
FILE_HEADER = [
    "experiment_name",
    "model",
    "cost"
]

"""OpenAI cost tracker"""
class OpenAICostTracker:
    def __init__(
        self,
        client: ClientType,
        model: str,
        input_cost: float,
        output_cost: float,
        experiment_name: str,
        cost_upperbound: float = float('inf'),
        log_folder: str = DEFAULT_LOG_PATH,
        client_args: Dict = {}
    ):
        """Initialize the cost tracker.

        Args:
            client (enum.ClientType): The client to use.
            model (str): The model to use.
            cost_upperbound (float): The upperbound of the cost after which an exception is raised.
            input_cost (float): The cost per million tokens for the input.
            output_cost (float): The cost per million tokens for the output.
            experiment_name (str): The name of the experiment.
            log_folder (str): The folder where to save the cost logs.
            client_args (Dict, optional): The parameters to pass to the client. Defaults to {}.
        """
        self.cost = 0
        self.model = model
        self.input_cost = input_cost
        self.log_folder = log_folder
        self.output_cost = output_cost
        self.experiment_name = experiment_name
        self.cost_upperbound = cost_upperbound
        self.filename = f"{experiment_name}_cost_" + strftime("%Y%m%d_%H%M%S") + ".csv"
        
        if client.value == ClientType.OPENAI.value:
            self.client = OpenAI(**client_args)
        elif client.value == ClientType.AZURE.value:
            self.client = AzureOpenAI(**client_args)
            
    def chat_completion(self, messages: List[Dict], api_args: Dict = {}) -> str:
        """Use the chat completion endpoint to get a response from the model
           and update the cost tracker with the cost of the completion.
           
        Args:
            messages (list): A list of messages to send to the model. Every message is a dictionary with the key 'role' and the value 'content'.
            api_args(Dict, optional): The parameters to pass to the api endpoint. Defaults to {}.
        Returns:
            str: The model's response.
        """
        answer = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **api_args
        )
        self.cost += self.__get_answer_cost(answer)
        self.__validate_cost()
        path = Path(self.log_folder, self.filename)
        path.parent.mkdir(parents=True, exist_ok=True)
    
        # Be careful, it overwrites the file if it already exists
        with open(path, mode='w') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(FILE_HEADER)
            csvwriter.writerow([self.experiment_name, self.model, self.cost])
        return answer.choices[0].message.content
        
    def __get_answer_cost(self, answer: Dict) -> float:
        """Calculate the cost of the answer based on the input and output tokens.

        Args:
            answer (dict): The response from the model.
        Returns:
            float: The cost of the answer.        
        """
        return (self.input_cost * answer.usage.prompt_tokens) / COST_UNIT + \
                    (self.output_cost * answer.usage.completion_tokens) / COST_UNIT
            
    def __validate_cost(self):
        """Check if the cost exceeds the upperbound and raise an exception if it does.

        Raises:
            Exception: If the cost exceeds the upperbound.
        """
        if self.cost > self.cost_upperbound:
            raise Exception(f"Cost exceeded upperbound: {self.cost} > {self.cost_upperbound}")        
            
    def get_current_cost(self) -> float:
        """Get the current cost of the cost tracker.

        Returns:
            float: The current cost.
        """
        return self.cost