# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/App_Description_Validator.ipynb.

# %% auto 0
__all__ = ['logger', 'ERROR_RESPONSE', 'GENERAL_FASTKAFKA_RESPONSE', 'validate_app_description']

# %% ../../nbs/App_Description_Validator.ipynb 1
from typing import *
import time

from yaspin import yaspin

from .._components.logger import get_logger
from .helper import CustomAIChat
from .prompts import APP_VALIDATION_PROMPT
from .constants import INCOMPLETE_DESCRIPTION, DESCRIPTION_EXAMPLE

# %% ../../nbs/App_Description_Validator.ipynb 3
logger = get_logger(__name__)

# %% ../../nbs/App_Description_Validator.ipynb 5
ERROR_RESPONSE = "I apologize, but I can only respond to queries related to FastStream code generation. Feel free to ask me about using FastStream, and I'll do my best to help you with that!"
GENERAL_FASTKAFKA_RESPONSE = "Great to see your interest in FastStream! Unfortunately, I can only generate FastStream code and offer assistance in that area. For general information about FastStream, please visit https://fastkafka.airt.ai/"

# %% ../../nbs/App_Description_Validator.ipynb 6
def validate_app_description(description: str, model: str, total_usage: List[Dict[str, int]]) -> Tuple[str, List[Dict[str, int]]]:
    """Validate the user's application description

    If the description is unrelated to FastStream or contains insensitive/inappropriate language, show an error
    message and exit the program. Otherwise, display the success message in the terminal.

    Args:
        description: User's application description
        
    Raises:
        ValueError: If the application description is invalid
    """
    
    print("✨  Generating a new FastStream application!")
    logger.info("==== App description validation ====")
    with yaspin(
        text="Validating the application description...", color="cyan", spinner="clock"
    ) as sp:
        
        ai = CustomAIChat(user_prompt=APP_VALIDATION_PROMPT, model=model, semantic_search_query="What is FastStream?")
        response, usage = ai(description)
        total_usage.append(usage)
        
        sp.text = ""
        if response == "0":
            raise ValueError(f"✘ Error: Application description validation failed.\n{ERROR_RESPONSE}\n{DESCRIPTION_EXAMPLE}\n\n")
        elif response == "1":
            raise ValueError(f"✘ Error: Application description validation failed.\n\n{GENERAL_FASTKAFKA_RESPONSE}\n{DESCRIPTION_EXAMPLE}\n\n")
        elif response == "2":
            raise ValueError(f"✘ Error: Application description is incomplete.\n\n{INCOMPLETE_DESCRIPTION}\n{DESCRIPTION_EXAMPLE}\n\n")
        else:
            sp.ok(" ✔ Application description validated.")
            return description, total_usage
