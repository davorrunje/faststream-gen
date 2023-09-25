# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/New_Project_Generator.ipynb.

# %% auto 0
__all__ = ['logger', 'create_project']

# %% ../../nbs/New_Project_Generator.ipynb 1
from typing import *
import shutil
from pathlib import Path
import os
from tempfile import TemporaryDirectory

from yaspin import yaspin

from .logger import get_logger
from faststream_gen._code_generator.helper import (
    download_and_extract_faststream_archive,
    write_file_contents,
    read_file_contents,
    CustomAIChat,
    ValidateAndFixResponse
)

from faststream_gen._code_generator.constants import (
    FASTSTREAM_TEMPLATE_ZIP_URL,
    FASTSTREAM_TEMPLATE_DIR_SUFFIX,
    INTERMEDIATE_RESULTS_DIR_NAME,
    APPLICATION_FILE_NAME,
    INTEGRATION_TEST_FILE_NAME,
    INTERMEDIATE_OUTPUT_DIR_NAME
)

from .._code_generator.prompts import REQUIREMENTS_GENERATION_PROMPT

# %% ../../nbs/New_Project_Generator.ipynb 3
logger = get_logger(__name__)

# %% ../../nbs/New_Project_Generator.ipynb 5
def _split_requirements(response: str) -> Tuple[str, str]:
    app_code, test_code = response.split("### requirements.txt ###")[1].split("### dev_requirements.txt ###")
    return app_code, test_code

def _validate_response(response: str) -> List[str]:
    try:
        requirements, dev_requirements = _split_requirements(response)
        return []
    except (IndexError, ValueError) as e:
        return [
            "Please add ### requirements.txt ### and ### dev_requirements.txt ### in your response"
        ]

# %% ../../nbs/New_Project_Generator.ipynb 8
def _generate_requirements(
    d: str, model: str, total_usage: List[Dict[str, int]]
) -> Tuple[str, str, List[Dict[str, int]]]:
    app_code = read_file_contents(f"{d}/app/application.py")
    requirements = read_file_contents(f"{d}/requirements.txt")
    dev_requirements = read_file_contents(f"{d}/dev_requirements.txt")

    prompt = (
        app_code
        + "\n==== REQUIREMENT ====\n"
        + requirements
        + "\n==== DEV REQUIREMENT ====\n"
        + dev_requirements
    )
    requirements_generator = CustomAIChat(
        model=model,
        user_prompt=REQUIREMENTS_GENERATION_PROMPT + prompt,
    )
    requirements_validator = ValidateAndFixResponse(
        requirements_generator, _validate_response
    )
    requirements, total_usage = requirements_validator.fix(
        prompt,
        total_usage=total_usage,
    )

    requirements, dev_requirements = _split_requirements(requirements)

    return requirements, dev_requirements, total_usage

# %% ../../nbs/New_Project_Generator.ipynb 10
def create_project(
    output_path: str,
    save_intermediate_files: bool,
    model: str,
    total_usage: List[Dict[str, int]],
) -> List[Dict[str, int]]:
    with yaspin(
        text="Creating a new FastStream project...", color="cyan", spinner="clock"
    ) as sp:
        with download_and_extract_faststream_archive(
            FASTSTREAM_TEMPLATE_ZIP_URL
        ) as extracted_path:
            with TemporaryDirectory() as tmp_dir:
                app_path = f"{tmp_dir}/app/application.py"
                test_path = f"{tmp_dir}/tests/test_application.py"

                intermediate_dir_path = f"{output_path}/{INTERMEDIATE_RESULTS_DIR_NAME}"
                intermediate_output_dir_path = f"{intermediate_dir_path}/{INTERMEDIATE_OUTPUT_DIR_NAME}"
                shutil.copytree(
                    str(extracted_path / FASTSTREAM_TEMPLATE_DIR_SUFFIX),
                    tmp_dir,
                    dirs_exist_ok=True,
                )
                shutil.copy(
                    f"{intermediate_output_dir_path}/{APPLICATION_FILE_NAME}", app_path
                )
                shutil.copy(
                    f"{intermediate_output_dir_path}/{INTEGRATION_TEST_FILE_NAME}", test_path
                )

                test_file_contents = read_file_contents(test_path)
                test_file_contents = test_file_contents.replace(
                    "from application import", "from app.application import"
                )
                write_file_contents(test_path, test_file_contents)

                requirements, dev_requirements, total_usage = _generate_requirements(tmp_dir, model, total_usage)

                requirements_file = f"{tmp_dir}/requirements.txt"
                write_file_contents(requirements_file, requirements)

                dev_requirements_file = f"{tmp_dir}/dev_requirements.txt"
                write_file_contents(dev_requirements_file, dev_requirements)

                shutil.copytree(tmp_dir, output_path, dirs_exist_ok=True)
                if not save_intermediate_files:
                    shutil.rmtree(intermediate_dir_path)

        sp.text = ""
        sp.ok(f" ✔ New FastStream project created.")
        return total_usage
