import os
from typing import Any
from dotenv import load_dotenv


load_dotenv()


def get_env_variable(name: str, default: Any = "") -> Any:
    env_var = os.environ.get(name)
    if env_var:
        return env_var if env_var not in {"False", "True"} else env_var == "True"
    return default