# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/App_And_Test_Generator.ipynb.

# %% auto 0
__all__ = ['logger', 'generate_app_and_test']

# %% ../../nbs/App_And_Test_Generator.ipynb 1
from typing import *
import time
import importlib.util
from tempfile import TemporaryDirectory
from pathlib import Path
import platform
import subprocess  # nosec: B404: Consider possible security implications associated with the subprocess module.

from yaspin import yaspin

from .._components.logger import get_logger
from faststream_gen._code_generator.helper import (
    CustomAIChat,
    ValidateAndFixResponse,
    write_file_contents,
    read_file_contents,
    validate_python_code,
)
from .prompts import APP_AND_TEST_GENERATION_PROMPT
from faststream_gen._code_generator.constants import (
    APPLICATION_SKELETON_FILE_NAME,
    APPLICATION_FILE_NAME,
    INTEGRATION_TEST_FILE_NAME,
)

# %% ../../nbs/App_And_Test_Generator.ipynb 3
logger = get_logger(__name__)

# %% ../../nbs/App_And_Test_Generator.ipynb 5
def _split_app_and_test_code(response: str) -> Tuple[str, str]:
    app_code, test_code = response.split("### application.py ###")[1].split("### test.py ###")
    return app_code, test_code


def _validate_response(response: str) -> List[str]:
    try:
        app_code, test_code = _split_app_and_test_code(response)
    except (IndexError, ValueError) as e:
        return [
            "Please add ### application.py ### and ### test.py ### in your response"
        ]
    with TemporaryDirectory() as d:
        write_file_contents(
            f"{d}/{APPLICATION_FILE_NAME}",
            app_code.replace("### application.py ###", ""),
        )

        test_file = f"{d}/{INTEGRATION_TEST_FILE_NAME}"
        write_file_contents(test_file, test_code)

        cmd = ["pytest", test_file, "--tb=short"]
        # nosemgrep: python.lang.security.audit.subprocess-shell-true.subprocess-shell-true
        p = subprocess.run(  # nosec: B602, B603 subprocess call - check for execution of untrusted input.
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True if platform.system() == "Windows" else False,
        )
        if p.returncode != 0:
            return [str(p.stdout.decode("utf-8"))]

        return []

# %% ../../nbs/App_And_Test_Generator.ipynb 9
def generate_app_and_test(
    description: str,
    model: str,
    code_gen_directory: str,
    total_usage: List[Dict[str, int]],
    relevant_prompt_examples: str,
) -> List[Dict[str, int]]:
    """Generate integration test for the FastStream app

    Args:
        description: Validated User application description
        code_gen_directory: The directory containing the generated files.
        relevant_prompt_examples: Relevant examples to add in the prompts.

    Returns:
        The generated integration test code for the application
    """
    logger.info("==== Skeleton to App and Test Generation ====")
    with yaspin(
        text="Generating application and tests (usually takes around 30 to 40 seconds)...", color="cyan", spinner="clock"
    ) as sp:
        app_file_name = f"{code_gen_directory}/{APPLICATION_SKELETON_FILE_NAME}"
        app_skeleton = read_file_contents(app_file_name)

        prompt = (
            APP_AND_TEST_GENERATION_PROMPT.replace(
                "==== REPLACE WITH APP DESCRIPTION ====", description
            )
            .replace("==== RELEVANT EXAMPLES GOES HERE ====", relevant_prompt_examples)
            .replace("from .app import", "from application import")
        )
        test_generator = CustomAIChat(
            params={
                "temperature": 0.5,
            },
            model=model,
            user_prompt=prompt,
            semantic_search_query="How to test FastStream applications? Explain in detail.",  # todo: experiment without this query
        )
        test_validator = ValidateAndFixResponse(test_generator, _validate_response)
        validated_app_and_test_code, total_usage = test_validator.fix(
            f"{app_skeleton}",
            total_usage=total_usage,
        )
        
        app_code, test_code = _split_app_and_test_code(validated_app_and_test_code)
        
        app_output_file = f"{code_gen_directory}/{APPLICATION_FILE_NAME}"
        write_file_contents(app_output_file, app_code)

        test_output_file = f"{code_gen_directory}/{INTEGRATION_TEST_FILE_NAME}"
        write_file_contents(test_output_file, test_code)

        sp.text = ""
        sp.ok(f" ✔ The app and the tests are generated.")
        return total_usage
