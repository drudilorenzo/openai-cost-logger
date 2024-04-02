1. ✅ cost tracker handles completion creation - PR ready

Change: separating completion and cost tracking, by changing the main functionality from `chat_completion` to `update_cost`

Motivation:
 - bulletproofs us from changes in how the completion is created, we only care about response structure
 - allows easier integration, user only has to initialize tracker object and call `update_cost(response)`, 
   otherwise each chat completion call would have to be rewritten 

2. ⌛ costs are calculated across all log files 

Change: 
 - static `total_cost` that will calculate total spending from logs
 - static `experiment_cost(experiment_name=self.experiment_name)` gets you total cost of specific experiment
  - defaulting to current experiment_name in tracker object
  - if object not initialized, experiment_name has to be provided
 - `cost` that gets you costs for current run of this tracker object

3. ⌛ log file just acumulates total cost

Change: 
 - add breakdown of responses/input token per response/output token per response/cost per response
 - maybe change log file format to json, so that we can better handle logs, for example:
    ```
    {
        "experiment_name"
        "model": 
        "run_datetime":
        "logs":
        {
            "0": {                                      # maybe datetime of response?
                "num_of_input_tokens": 
                "num_of_output_tokens":
                "other":                                # additional info? message? thread? prompt?
            }
        }
        "total": {
            "cost":                                     # something else?
        }
    }
    ```

4. ⌛ model has to be provided in form of enum

Change:
    - we can just infer it from `response.model`
    - removes possible problems with choosing the right enum or forgetting to change it while changing the model for experiment

5. ⌛ datetime strftime format

Change: 
 - change strftime format to `strftime("%Y-%m-%d_%H:%M:%S")`, makes it more readable
 - we could possibly infer the datetime and do plots with datetime instead of str

6. WIP
