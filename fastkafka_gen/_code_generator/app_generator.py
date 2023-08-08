# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/App_Generator.ipynb.

# %% auto 0
__all__ = ['logger', 'ENTITY_PROMPT', 'generate_app']

# %% ../../nbs/App_Generator.ipynb 1
from typing import *
import time

from yaspin import yaspin

from fastkafka._components.logger import get_logger
from fastkafka._code_generator.helper import CustomAIChat, ValidateAndFixResponse
from fastkafka._code_generator.prompts import APP_GENERATION_PROMPT

# %% ../../nbs/App_Generator.ipynb 3
logger = get_logger(__name__)

# %% ../../nbs/App_Generator.ipynb 5
ENTITY_PROMPT = """{entities}
{arguments}
"""


def _generate_entities_string(plan: Dict[str, List[Dict[str, Any]]]) -> str:
    entities = "\n".join([entity["name"] for entity in plan["entities"]])
    arguments = "\n".join(
        f"\nLet's now implement the {entity['name']} class with the following arguments:\n"
        + "\n".join(f"Argument: {k}, Type: {v}" for k, v in entity["arguments"].items())
        for entity in plan["entities"]
    )

    return ENTITY_PROMPT.format(entities=entities, arguments=arguments)

# %% ../../nbs/App_Generator.ipynb 8
def _get_functions_prompt(
    functions: Dict[str, Dict[str, Union[str, List[Any]]]],
    app_name: str,
    is_producer_function: bool = False,
) -> str:
    function_messages = []
    for k, v in functions.items():
        parameters = ", ".join(
            [
                f"Parameter: {param_name}, Type: {param_type}"
                for parameter in v["parameters"]
                for param_name, param_type in parameter.items()
            ]
        )
        function_message = f"""
Now lets write the following @{app_name}.consumes functions with the following details:

Write a consumes function named "{k}" which should consume messages from the "{v['topic']}" topic and set the prefix parameter to "{v['prefix']}".
The function should take the following parameters:
{parameters}

The function should implement the following business logic:
{v['description']}"""

        if is_producer_function:
            function_message += f'\n\nAfter implementing the above logic, the function should return the {v["returns"]} object.'
            function_message = function_message.replace("consumes function", "produces function").replace("which should consume messages from the", "which should produce messages to the")

        function_messages.append(function_message)

    return "\n".join(function_messages)

# %% ../../nbs/App_Generator.ipynb 12
def _generate_apps_prompt(plan: Dict[str, List[Dict[str, Any]]]) -> str:
    apps_prompt = ""
    for app in plan["apps"]:
        apps_prompt += f"""Now, lets create a instance of the FastKafka app with the following fields and assign it to the variable named {app['app_name']}:

kafka_brokers: {app["kafka_brokers"]}
title: {app["title"]}
{_get_functions_prompt(app["produces_functions"], app["app_name"], True)}
{_get_functions_prompt(app["consumes_functions"], app["app_name"])}

"""
    return apps_prompt

# %% ../../nbs/App_Generator.ipynb 15
def _generate_app_prompt(plan: str) -> str:
    plan_dict = json.loads(plan)
    entities_prompt = _generate_entities_string(plan_dict)
    apps_prompt = _generate_apps_prompt(plan_dict)
    generated_plan_prompt = entities_prompt + "\n\n" + apps_prompt
    return APP_GENERATION_PROMPT.format(generated_plan_prompt=generated_plan_prompt)

# %% ../../nbs/App_Generator.ipynb 17
def _validate_response(response: str) -> str:
    # todo:
    return []

# %% ../../nbs/App_Generator.ipynb 20
def generate_app(plan: str, description: str) -> Tuple[str, str]:
    """Generate code for the new FastKafka app from the validated plan
    
    Args:
        plan: The validated application plan generated from the user's application description
        description: Validated user's application description
    Returns:
        The generated FastKafka code
    """
    # TODO: Generate code form the plan prompt
    # TODO: Validate the generated code
    with yaspin(text="Generating FastKafka app...", color="cyan", spinner="clock") as sp:
        app_prompt = _generate_app_prompt(plan)
        
        app_generator = CustomAIChat(user_prompt=app_prompt)
        app_validator = ValidateAndFixResponse(app_generator, _validate_response)
        validated_app, total_tokens = app_validator.fix(description)
        
        sp.text = ""
        sp.ok(" ✔ FastKafka app generated and saved at: /some_dir/application.py")
        return validated_app, total_tokens
