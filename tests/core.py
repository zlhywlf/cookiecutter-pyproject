from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from cookiecutter.hooks import run_script as real_run_script
from cookiecutter.main import cookiecutter
from jinja2 import Environment

from hooks.pre_prompt import main

if TYPE_CHECKING:
    from pathlib import Path

    import py
    from _typeshed import DataclassInstance


@dataclass(frozen=True)
class Result:
    """Represents the result of a command execution.

    This data class holds information about the outcome of a command execution, including any exceptions,
    exit codes, and the project directory if applicable. It is immutable due to the `frozen=True` parameter.

    Attributes:
        exception: An exception or SystemExit object if an error occurred during command execution, or None if no error.
        exit_code: The exit code of the command execution, can be a string or integer, or None if not applicable.
        project_dir: The path to the project directory created by the command, or None if no project was created.
    """

    exception: Exception | SystemExit | None = None
    exit_code: str | int | None = None
    project_dir: str | None = None


class Baker:
    """A utility class for baking projects using Cookiecutter templates.

    This class encapsulates the logic for generating projects from Cookiecutter templates, handling configuration,
    and managing output directories. It provides a `bake` method to execute the template rendering process.

    Attributes:
        template_path (Path): The path to the Cookiecutter template directory.
        output_path (py.path.local): The path to the output directory where the generated project will be placed.
        config_path (py.path.local): The path to the configuration file used by Cookiecutter.
    """

    def __init__(self, template_path: Path, output_path: py.path.local, config_path: py.path.local) -> None:
        """Initialize the Baker instance with the necessary paths.

        Args:
            template_path (Path): Path to the Cookiecutter template directory.
            output_path (py.path.local): Path to the output directory for the generated project.
            config_path (py.path.local): Path to the configuration file used by Cookiecutter.
        """
        self.template_path = template_path
        self.output_path = output_path
        self.config_path = config_path

    def bake(self, context: DataclassInstance) -> Result:
        """Generate a project from the provided context using the specified Cookiecutter template.

        This method renders the template with the given context, handles any templated strings within the context,
        and returns a `Result` object containing the outcome of the operation.

        Args:
            context (DataclassInstance): An instance of a dataclass containing the context data for the template.

        Returns:
            Result: A `Result` object containing information about the outcome of the bake operation, including any
                    exceptions, exit codes, and the path to the generated project directory.
        """
        extra_context = asdict(context)
        project_dir = cookiecutter(
            self.template_path.absolute().as_posix(),
            no_input=True,
            extra_context=extra_context,
            output_dir=self.output_path.strpath,
            config_file=self.config_path.strpath,
        )

        # Post-process any templated strings in the context
        for k, v in extra_context.items():
            if isinstance(v, str) and "{{" in v and "}}" in v:
                real = Environment(autoescape=True).from_string(v).render(cookiecutter=extra_context)
                setattr(context, k, real)

        return Result(exception=None, exit_code=0, project_dir=project_dir)


def run_script(script_path: str, cwd: Path) -> None:
    """Run a script with special handling for pre_prompt.py.

    This function executes the specified script. If the script is `pre_prompt.py`, it changes the current working
    directory to `cwd` and calls the `main` function directly. For other scripts, it delegates the execution to
    `real_run_script`.

    Args:
        script_path (str): The path to the script to be executed.
        cwd (Path): The current working directory to use when executing the script.

    Notes:
        - Handles `pre_prompt.py` specially by invoking its `main` function directly.
        - For other scripts, uses `real_run_script` for execution.
    """
    if "pre_prompt.py" in script_path:
        os.chdir(cwd)
        main()
    else:
        real_run_script(script_path, cwd)
