"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib

from hooks.context import Context


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
