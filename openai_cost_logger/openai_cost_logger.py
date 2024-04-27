import json
import warnings
from typing import Dict
from pathlib import Path
from time import strftime
from openai._models import BaseModel # all the api responses extend BaseModel

from openai_cost_logger.constants import DEFAULT_LOG_PATH, MODELS_COST


"""Every cost is per million tokens."""
COST_UNIT = 1_000_000


"""OpenAI cost logger."""
class OpenAICostLogger:
    def __init__(
        self,
        experiment_name: str,
        cost_upperbound: float = float('inf'),
        log_folder: str = DEFAULT_LOG_PATH,
        log_level: str = "detail"
    ):
        """Initialize the cost logger.

        Args:
            experiment_name (str): The name of the experiment.
            cost_upperbound (float): The upperbound of the cost after which an exception is raised.
            log_folder (str): The folder where to save the cost logs.
            log_level (str): The level of logging. # TODO: implement logging levels.
        """
        self.cost = 0
        self.n_responses = 0
        self.log_folder = log_folder
        self.experiment_name = experiment_name
        self.cost_upperbound = cost_upperbound
        self.log_level = log_level
        self.creation_datetime = strftime("%Y-%m-%d_%H:%M:%S")
        self.filename = f"{experiment_name}_{self.creation_datetime}.json"
        self.filepath = Path(self.log_folder, self.filename)

        self.__check_existance_log_folder()
        self.__build_log_file()


    def update_cost(self, response: BaseModel, input_cost: float = None, output_cost: float = None) -> None:
        """Extract the cost from the response and update the cost tracker.
           Then write the cost to the json file for temporary storage.
           
           Be aware that:
           - the cost is calculated per million tokens.
           - if input_cost and output_cost are not provided, the cost tracker will search for the values in the default dictionary.
             In case the values are not found, the cost tracker will raise an exception.
        
        Args:
            response (BaseModel): BaseModel object from the model.
            input_cost (float, optional): The cost per million tokens for the input. Defaults to None.
            output_cost (float, optional): The cost per million tokens for the output. Defaults to None.
        """
        if (input_cost is None or output_cost is None) and response.model not in MODELS_COST:
            raise Exception(f"Model {response.model} not found in the cost dictionary. Please provide the input and output cost.")
        
        input_cost = MODELS_COST[response.model]["input"] if input_cost is None else input_cost
        output_cost = MODELS_COST[response.model]["output"] if output_cost is None else output_cost
        self.cost += self.__get_answer_cost(response=response, input_cost=input_cost, output_cost=output_cost)
        self.n_responses += 1
        self.__write_cost_to_json(response=response, input_cost=input_cost, output_cost=output_cost)
        self.__validate_cost()

        
    def get_current_cost(self) -> float:
        """Get the current cost of the cost tracker.

        Returns:
            float: The current cost.
        """
        return self.cost
    
    
    def __get_answer_cost(self, response: BaseModel, input_cost: float, output_cost: float) -> float:
        """Calculate the cost of the response based on the input and output tokens.

        Args:
            response (BaseModel): The response from the model.
            input_cost (float): The cost per million tokens for the input.
            output_cost (float): The cost per million tokens for the output.
        Returns:
            float: The cost of the answer.     
        Raises:
            RuntimeWarning: If the output cost is 0 and there are completion tokens.   
        """
        completion_tokens = response.usage.total_tokens - response.usage.prompt_tokens
                
        if completion_tokens != 0 and output_cost == 0:
            warnings.warn(f"Output cost: {output_cost}. Found {completion_tokens} completion tokens.", RuntimeWarning)
            
        return (input_cost * response.usage.prompt_tokens) / COST_UNIT + (output_cost * completion_tokens) / COST_UNIT
            
            
    def __validate_cost(self):
        """Check if the cost exceeds the upperbound and raise an exception if it does.

        Raises:
            Exception: If the cost exceeds the upperbound.
        """
        if self.cost > self.cost_upperbound: 
            raise Exception(f"Cost exceeded upperbound: {self.cost} > {self.cost_upperbound}")


    def __write_cost_to_json(self, response: BaseModel, input_cost: float, output_cost: float) -> None:
        """Write the cost to the json file. 

        Args:
            response (BaseModel): The response from the model.
            input_cost (float): The cost per million tokens for the input.
            output_cost (float): The cost per million tokens for the output.
        """
        with open(self.filepath, 'r') as file:
            data = json.load(file)
            data["total_cost"] = self.cost
            data["total_responses"] = self.n_responses
            data["breakdown"].append(self.__build_log_breadown_entry(
                response=response,
                input_cost=input_cost,
                output_cost=output_cost
            ))
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)


    def __check_existance_log_folder(self) -> None:
        """Check if the log folder exists and create it if it does not."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)


    def __build_log_file(self) -> None:
        """Create the log file with the header."""
        log_file_template = {
            "experiment_name": self.experiment_name,
            "creation_datetime": strftime("%Y-%m-%d %H:%M:%S"),
            "total_cost": self.cost,
            "total_responses": 0,
            "breakdown": []
        }
        with open(self.filepath, 'w') as file:
            json.dump(log_file_template, file, indent=4)

    
    def __build_log_breadown_entry(self, response: BaseModel, input_cost: float, output_cost: float) -> Dict:
        """Build a json log entry for the breakdown of the cost.
        
           Be aware that:
           - The content of the response is supported only for the completion models.

        Args:
            response (BaseModel): The response from the model.
            input_cost (float): The cost per million tokens for the input.
            output_cost (float): The cost per million tokens for the output.
        Returns:
            Dict: The json log entry.
        """
        output_tokens = response.usage.total_tokens - response.usage.prompt_tokens
        content = response.choices[0].message.content if hasattr(response, "choices") else "content-not-supported-for-this-model"
        return {
            "model": response.model,
            "cost": self.__get_answer_cost(response=response, input_cost=input_cost, output_cost=output_cost),
            "input_cost_per_million": input_cost,
            "output_cost_per_million": output_cost,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": output_tokens,
            "content": content,
            "datetime": strftime("%Y-%m-%d %H:%M:%S"),
        }