"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel


class Context(BaseModel):
    """Consistent with cookiecutter.json."""

    project_name: str
    project_slug: str
    author: str
