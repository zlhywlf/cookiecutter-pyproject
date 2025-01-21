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
    """result."""

    exception: Exception | SystemExit | None = None
    exit_code: str | int | None = None
    project_dir: str | None = None


class Baker:
    """baker."""

    def __init__(self, template_path: Path, output_path: py.path.local, config_path: py.path.local) -> None:
        """Init."""
        self.template_path = template_path
        self.output_path = output_path
        self.config_path = config_path

    def bake(self, context: DataclassInstance) -> Result:
        """Generate project files.

        Returns:
            Result
        """
        extra_context = asdict(context)
        project_dir = cookiecutter(
            self.template_path.absolute().as_posix(),
            no_input=True,
            extra_context=extra_context,
            output_dir=self.output_path.strpath,
            config_file=self.config_path.strpath,
        )

        for k, v in extra_context.items():
            if isinstance(v, str) and "{{" in v and "}}" in v:
                real = Environment(autoescape=True).from_string(v).render(cookiecutter=extra_context)
                setattr(context, k, real)
        return Result(exception=None, exit_code=0, project_dir=project_dir)


def run_script(script_path: str, cwd: Path) -> None:
    """Execute a script from a working directory."""
    if "pre_prompt.py" in script_path:
        os.chdir(cwd)
        main()
    else:
        real_run_script(script_path, cwd)
