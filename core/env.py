"""
ENVIRONMENT VARIABLES
"""
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
import os


def load_env() -> bool:
    """Load environment variables from .env file."""
    env_path = Path('.') / '.env'
    if not env_path.exists():
        env_path = Path('..') / '.env'
        if not env_path.exists():
            env_path.touch()

    return load_dotenv(dotenv_path=env_path)


def env(param: str, default: Any = None) -> Any:
    """Get environment variable or return default value."""
    val = os.environ.get(param, default)
    if val is None:
        load_env()
    return os.environ.get(param, default)
