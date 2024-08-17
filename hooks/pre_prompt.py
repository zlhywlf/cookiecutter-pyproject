"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel


class Context(BaseModel):
    """cookiecutter context."""

    project_name: str = f'Python Project {datetime.now(tz=timezone(timedelta(hours=8))).strftime("%Y%m%d%H%M%S")}'
    project_slug: str = "{{ cookiecutter.project_name.lower().replace(' ', '_') }}"
    author: str = "Anonymous"


def generate_context() -> None:
    """Generate cookiecutter.json."""
    context = Context()
    with pathlib.Path("cookiecutter.json").open("w") as file:
        file.write(context.model_dump_json())


def main() -> None:
    """Pre prompt hook."""
    generate_context()


if __name__ == "__main__":
    main()
