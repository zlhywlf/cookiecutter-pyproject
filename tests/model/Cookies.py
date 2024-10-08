"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, Callable, Optional, Union

import py
from cookiecutter.main import cookiecutter
from jinja2 import Environment
from pydantic import BaseModel

from tests.model.Result import Result


class Cookies:
    """Class to provide convenient access to the cookiecutter API."""

    def __init__(self, template: str, output_factory: Callable[..., Any], config_file: py.path.local) -> None:
        """Init."""
        self._default_template = template
        self._output_factory = output_factory
        self._config_file = config_file
        self._counter = 0

    def _new_output_dir(self) -> py.path.local:
        """Obtain the generation path."""
        dirname = f"bake{self._counter:02d}"
        output_dir = self._output_factory(dirname)
        self._counter += 1
        return output_dir

    def bake(self, context: BaseModel) -> Result:
        """Generate project files."""
        exception: Optional[Union[Exception, SystemExit]] = None
        exit_code: Optional[Union[str, int]] = 0
        project_dir = None
        extra_context = context.model_dump()
        try:
            project_dir = cookiecutter(
                self._default_template,
                no_input=True,
                extra_context=extra_context,
                output_dir=str(self._new_output_dir()),
                config_file=str(self._config_file),
            )

            for k, v in extra_context.items():
                if isinstance(v, str) and "{{" in v and "}}" in v:
                    real = Environment(autoescape=True).from_string(v).render(cookiecutter=extra_context)
                    setattr(context, k, real)
        except SystemExit as e:
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:  # noqa: BLE001
            exception = e
            exit_code = -1
        return Result(exception=exception, exit_code=exit_code, project_dir=project_dir)
