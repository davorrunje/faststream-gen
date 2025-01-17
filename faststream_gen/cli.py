# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/CLI.ipynb.

# %% auto 0
__all__ = ['logger', 'OPENAI_KEY_EMPTY_ERROR', 'OPENAI_KEY_NOT_SET_ERROR', 'app', 'EMPTY_DESCRIPTION_ERROR',
           'generate_fastkafka_app']

# %% ../nbs/CLI.ipynb 1
from typing import *
import os
import re

import typer
import pathlib

from ._components.logger import get_logger
from faststream_gen._code_generator.app_description_validator import (
    validate_app_description,
)

# from faststream_gen._code_generator.asyncapi_spec_generator import generate_asyncapi_spec
from ._code_generator.app_skeleton_generator import generate_app_skeleton
from ._code_generator.app_and_test_generator import generate_app_and_test
from ._components.integration_test_generator import run_integration_test
from faststream_gen._code_generator.helper import (
    set_logger_level,
    add_tokens_usage,
    write_file_contents,
    get_relevant_prompt_examples,
)
from faststream_gen._code_generator.constants import (
    MODEL_PRICING,
    TOKEN_TYPES,
    DESCRIPTION_FILE_NAME,
    GENERATE_APP_FROM_ASYNCAPI,
    GENERATE_APP_SKELETON,
    LOGS_DIR_NAME,
    OpenAIModel,
    LOG_OUTPUT_DIR_NAME,
    INCOMPLETE_APP_ERROR_MSG,
)

from ._components.new_project_generator import create_project

# %% ../nbs/CLI.ipynb 3
logger = get_logger(__name__)

# %% ../nbs/CLI.ipynb 6
OPENAI_KEY_EMPTY_ERROR = "Error: OPENAI_API_KEY cannot be empty. Please set a valid OpenAI API key in OPENAI_API_KEY environment variable and try again.\nYou can generate API keys in the OpenAI web interface. See https://platform.openai.com/account/api-keys for details."
OPENAI_KEY_NOT_SET_ERROR = "Error: OPENAI_API_KEY not found in environment variables. Set a valid OpenAI API key in OPENAI_API_KEY environment variable and try again. You can generate API keys in the OpenAI web interface. See https://platform.openai.com/account/api-keys for details."


def _ensure_openai_api_key_set() -> None:
    """Ensure the 'OPENAI_API_KEY' environment variable is set and is not empty.

    Raises:
        KeyError: If the 'OPENAI_API_KEY' environment variable is not found.
        ValueError: If the 'OPENAI_API_KEY' environment variable is found but its value is empty.
    """
    try:
        openai_api_key = os.environ["OPENAI_API_KEY"]
        if openai_api_key == "":
            raise ValueError(OPENAI_KEY_EMPTY_ERROR)
    except KeyError:
        raise KeyError(OPENAI_KEY_NOT_SET_ERROR)

# %% ../nbs/CLI.ipynb 10
app = typer.Typer(
    short_help="Commands for accelerating FastStream project creation using advanced AI technology",
     help="""Commands for accelerating FastStream project creation using advanced AI technology.

These commands use OpenAI's model to generate FastStream project. To access this feature, kindly sign up if you haven't already and create an API key with OpenAI. You can generate API keys in the OpenAI web interface. See https://platform.openai.com/account/api-keys for details.

Once you have the key, please set it in the OPENAI_API_KEY environment variable before executing the code generation commands.

Note: Accessing OpenAI API incurs charges. For further information on pricing and free credicts, check this link: https://openai.com/pricing
    """,
)

# %% ../nbs/CLI.ipynb 11
def _strip_white_spaces(description: str) -> str:
    """Remove and strip excess whitespaces from a given description

    Args:
        description: The description string to be processed.

    Returns:
        The cleaned description string.
    """
    pattern = re.compile(r"\s+")
    return pattern.sub(" ", description).strip()

# %% ../nbs/CLI.ipynb 13
def _calculate_price(total_tokens_usage: Dict[str, int], model: str) -> float:
    """Calculates the total price based on the number of promt & completion tokens and the models price for input and output tokens (per 1k tokens).

    Args:
        total_tokens_usage: OpenAI "usage" dictionaries which defines prompt_tokens, completion_tokens and total_tokens


    Returns:
        float: The price for used tokens
    """
    model_price = MODEL_PRICING[model]
    price = (total_tokens_usage["prompt_tokens"] * model_price["input"] + total_tokens_usage["completion_tokens"] * model_price["output"]) / 1000
    return price

# %% ../nbs/CLI.ipynb 15
EMPTY_DESCRIPTION_ERROR = "Error: you need to provide the application description by providing it with the command line argument or by providing it within a textual file wit the --input_file argument."

def _get_description(input_path: str) -> str:
    """Reads description from te file and returns it as a string

    Args:
        input_path: Path to the file with the desription
        
    Raises:
        ValueError: If the file does not exist.

    Returns:
        The description string which was read from the file.
    """
    try:
        with open(input_path) as file:
            # Read all lines to list
            lines = file.readlines()
            # Join the lines 
            description = '\r'.join(lines)
            logger.info(f"Reading application description from '{str(pathlib.Path(input_path).absolute())}'.")
    except Exception as e:
        raise ValueError(f"Error while reading from the file: '{str(pathlib.Path(input_path).absolute())}'\n{str(e)}")
    return description

# %% ../nbs/CLI.ipynb 18
@app.command(
    "generate",
    help="Effortlessly create a new FastStream project based on the app description.",
)
@set_logger_level
def generate_fastkafka_app(
    description: Optional[str] = typer.Argument(
        None,
        help="""Summarize your FastStream application in a few sentences!


\nInclude details about messages, topics, servers, and a brief overview of the intended business logic.


\nThe simpler and more specific the app description is, the better the generated app will be. Please refer to the below example for inspiration:


\nCreate a FastStream application using localhost broker for testing and use the default port number. 
It should consume messages from the "input_data" topic, where each message is a JSON encoded object containing a single attribute: 'data'. 
For each consumed message, create a new message object and increment the value of the data attribute by 1. Finally, send the modified message to the 'output_data' topic.
\n""",
    ),
    input_path: str = typer.Option(
        None,
        "--input_file",
        "-i",
        help="""
        The path to the file with the app desription. This path should be relative to the current working directory.
        
        \n\nIf the app description is passed via both a --input_file and a command line argument, the description from the command line will be used to create the application.
        """,
    ),
    output_path: str = typer.Option(
        ".",
        "--output_path",
        "-o",
        help="The path to the output directory where the generated project files will be saved. This path should be relative to the current working directory.",
    ),
    model: OpenAIModel = typer.Option(
        OpenAIModel.gpt3.value,
        "--model",
        "-m",
        help=f"The OpenAI model that will be used to create the FastStream project. For better results, we recommend using '{OpenAIModel.gpt4.value}'.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging by setting the logger level to INFO.",
    ),
    save_log_files: bool = typer.Option(
        False,
        "--dev",
        "-d",
        help="Save the complete logs generated by faststream-gen inside the output_path directory.",
    ),
) -> None:
    """Effortlessly create a new FastStream project based on the app description."""
    logger.info("Project generation started.")
    try:
        tokens_list: List[Dict[str, int]] = []
        _ensure_openai_api_key_set()
        if not description:
            if not input_path:
                raise ValueError(EMPTY_DESCRIPTION_ERROR)
            description = _get_description(input_path)

        cleaned_description = _strip_white_spaces(description)
        validated_description, tokens_list = validate_app_description(
            cleaned_description, model.value, tokens_list
        )
        intermediate_results_path = (
            pathlib.Path(output_path) / LOGS_DIR_NAME
        )
        intermediate_output_path = (
            intermediate_results_path / LOG_OUTPUT_DIR_NAME
        )
        intermediate_output_path.mkdir(parents=True, exist_ok=True)

        write_file_contents(
            f"{intermediate_output_path}/{DESCRIPTION_FILE_NAME}",
            validated_description,
        )

        #         tokens_list = generate_asyncapi_spec(validated_description, output_path, tokens_list)
        #         tokens_list = generate_app(output_path, tokens_list, GENERATE_APP_FROM_ASYNCAPI)

        prompt_examples = get_relevant_prompt_examples(validated_description)
        tokens_list = generate_app_skeleton(
            str(intermediate_results_path),
            model.value,
            tokens_list,
            prompt_examples["description_to_skeleton"],
        )

        tokens_list, is_app_and_test_code_broken = generate_app_and_test(
            validated_description,
            model.value,
            str(intermediate_results_path),
            tokens_list,
            prompt_examples["skeleton_to_app_and_test"],
        )

        tokens_list = create_project(
            output_path,
            save_log_files,
            model.value,
            tokens_list,
            is_app_and_test_code_broken,
        )

        run_integration_test(output_path)

    except (ValueError, KeyError) as e:
        fg = typer.colors.RED
        typer.secho(e, err=True, fg=fg)
        raise typer.Exit(code=1)
    except Exception as e:
        fg = typer.colors.RED
        typer.secho(f"Unexpected internal error: {e}", err=True, fg=fg)
        raise typer.Exit(code=1)
    finally:
        total_tokens_usage = add_tokens_usage(tokens_list)
        price = _calculate_price(total_tokens_usage, model.value)

        fg = typer.colors.CYAN
        typer.secho(f" Tokens used: {total_tokens_usage['total_tokens']}", fg=fg)
        logger.info(f"Prompt Tokens: {total_tokens_usage['prompt_tokens']}")
        logger.info(f"Completion Tokens: {total_tokens_usage['completion_tokens']}")
        typer.secho(f" Total Cost (USD): ${round(price, 5)}", fg=fg)

    #         phases = [
    #             "validation",
    #             "specification generation",
    #             "app generation",
    #             "test generation",
    #         ]
    #         logger.info("Number of tokens per phase:")
    #         for i, token in enumerate(tokens_list):
    #             logger.info(f"{phases[i]}: {token['total_tokens']} tokens")

    if is_app_and_test_code_broken:
        if output_path == ".":
            test_cmd = "python -m pytest"
            logs_dir = LOGS_DIR_NAME
        else:
            test_cmd = f"cd {output_path} && python -m pytest"
            logs_dir = f"{output_path}/{LOGS_DIR_NAME}"
        typer.secho(
            f"""\n\n{INCOMPLETE_APP_ERROR_MSG}

{test_cmd}

For in-depth debugging, check the {logs_dir} directory for complete logs, including individual step information.
""",
            fg=typer.colors.RED,
        )
    else:
        typer.secho("✨  All files were successfully generated!", fg=fg)
