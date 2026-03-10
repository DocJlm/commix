"""commix - AI-Powered Smart Git Commit Assistant

A CLI tool that uses AI to generate intelligent, conventional commit messages.
"""

__version__ = "0.1.0"
__author__ = "DocJlm"
__license__ = "MIT"

from .cli import app
from .generator import CommitGenerator

__all__ = ["app", "CommitGenerator", "__version__"]
