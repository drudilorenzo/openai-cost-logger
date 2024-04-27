1. ✅ model has to be provided in form of enum - important, hard to juggle with all 0xxx versions  - Merged

Change:
    - we can just infer it from `response.model`
    - removes possible problems with choosing the right enum or forgetting to change it while changing the model for experiment

2. ⌛ allow for experiment/subexperiment stats

3. ✅ cost tracker handles completion creation - Merged

Change: separating completion and cost tracking, by changing the main functionality from `chat_completion` to `update_cost`

Motivation:
 - bulletproofs us from changes in how the completion is created, we only care about response structure
 - allows easier integration, user only has to initialize tracker object and call `update_cost(response)`, 
   otherwise each chat completion call would have to be rewritten 

4. ✅ log file just acumulates total cost - Merged

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

5. ✅ datetime strftime format - Merged

Change: 
 - change strftime format to `strftime("%Y-%m-%d_%H:%M:%S")`, makes it more readable
 - we could possibly infer the datetime and do plots with datetime instead of str

6. ⌛ web ui for stats viz

7. WIP
