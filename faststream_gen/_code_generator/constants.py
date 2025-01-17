# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Constants.ipynb.

# %% auto 0
__all__ = ['DESCRIPTION_FILE_NAME', 'APPLICATION_SKELETON_FILE_NAME', 'ASYNC_API_SPEC_FILE_NAME', 'APPLICATION_FILE_NAME',
           'INTEGRATION_TEST_FILE_NAME', 'LOGS_DIR_NAME', 'LOG_OUTPUT_DIR_NAME', 'GENERATE_APP_FROM_ASYNCAPI',
           'GENERATE_APP_FROM_SKELETON', 'GENERATE_APP_SKELETON', 'RESULTS_DIR_NAMES', 'DEFAULT_PARAMS', 'MAX_RETRIES',
           'MAX_RESTARTS', 'MAX_ASYNC_SPEC_RETRIES', 'TOKEN_TYPES', 'MODEL_PRICING', 'INCOMPLETE_DESCRIPTION',
           'DESCRIPTION_EXAMPLE', 'MAX_NUM_FIXES_MSG', 'INCOMPLETE_APP_ERROR_MSG', 'FASTSTREAM_REPO_ZIP_URL',
           'FASTSTREAM_DOCS_DIR_SUFFIX', 'FASTSTREAM_EXAMPLES_DIR_SUFFIX', 'FASTSTREAM_EXAMPLE_FILES',
           'FASTSTREAM_TMP_DIR_PREFIX', 'FASTSTREAM_DIR_TO_EXCLUDE', 'FASTSTREAM_TEMPLATE_ZIP_URL',
           'FASTSTREAM_TEMPLATE_DIR_SUFFIX', 'OpenAIModel']

# %% ../../nbs/Constants.ipynb 2
from enum import Enum

# %% ../../nbs/Constants.ipynb 3
DESCRIPTION_FILE_NAME = "app_description.txt"
APPLICATION_SKELETON_FILE_NAME = "application_skeleton.py"
ASYNC_API_SPEC_FILE_NAME = "asyncapi.yml"
APPLICATION_FILE_NAME = "application.py"
INTEGRATION_TEST_FILE_NAME = "test.py"
LOGS_DIR_NAME = "_faststream_gen_logs"
LOG_OUTPUT_DIR_NAME = "output_dir"

GENERATE_APP_FROM_ASYNCAPI = "generate_app_from_asyncapi"
GENERATE_APP_FROM_SKELETON = "generate_app_from_skeleton"
GENERATE_APP_SKELETON = "generate_app_skeleton"

RESULTS_DIR_NAMES = {
    "skeleton": "app-skeleton-generation-logs",
    "app": "app-and-test-generation-logs"
}

# %% ../../nbs/Constants.ipynb 5
DEFAULT_PARAMS = {
    "temperature": 0.7,
}

MAX_RETRIES = 3
MAX_RESTARTS = 3
MAX_ASYNC_SPEC_RETRIES = 3



class OpenAIModel(str, Enum):
    gpt3 = "gpt-3.5-turbo-16k"
    gpt4 = "gpt-4"


# %% ../../nbs/Constants.ipynb 8
TOKEN_TYPES = ["prompt_tokens", "completion_tokens", "total_tokens"]

MODEL_PRICING = {
    OpenAIModel.gpt4.value: {
        "input": 0.03,
        "output": 0.06
    },
    OpenAIModel.gpt3.value: {
        "input": 0.003,
        "output": 0.004
    },
}

# %% ../../nbs/Constants.ipynb 10
INCOMPLETE_DESCRIPTION = """Please check if your application description is missing some crucial information:
- Description of the messages that will be produced or consumed
- At least one topic
- The business logic to implement while consuming or producing the messages
"""
DESCRIPTION_EXAMPLE = """
If you're unsure about how to construct the app description, consider the following example for guidance

APPLICATION DESCRIPTION EXAMPLE:
Create a FastStream application using localhost broker for testing and use the default port number. 
It should consume messages from the 'input_data' topic, where each message is a JSON encoded object containing a single attribute: 'data'. 
For each consumed message, create a new message object and increment the value of the data attribute by 1. Finally, send the modified message to the 'output_data' topic.
"""

MAX_NUM_FIXES_MSG = "Maximum number of retries"

INCOMPLETE_APP_ERROR_MSG = """Apologies, we couldn't generate a working application and test code from your application description.

Please run the following command to start manual debugging:
"""

# %% ../../nbs/Constants.ipynb 12
FASTSTREAM_REPO_ZIP_URL = "http://github.com/airtai/faststream/archive/main.zip"
FASTSTREAM_DOCS_DIR_SUFFIX = "faststream-main/.faststream_gen"
FASTSTREAM_EXAMPLES_DIR_SUFFIX = "faststream-main/faststream_gen_examples"
FASTSTREAM_EXAMPLE_FILES = ['description.txt', 'app_skeleton.py', 'app.py', 'test_app.py']
FASTSTREAM_TMP_DIR_PREFIX = "appended_examples"
FASTSTREAM_DIR_TO_EXCLUDE = "api"

# %% ../../nbs/Constants.ipynb 14
FASTSTREAM_TEMPLATE_ZIP_URL = "http://github.com/airtai/faststream-gen-template/archive/main.zip"
FASTSTREAM_TEMPLATE_DIR_SUFFIX = "faststream-gen-template-main"
