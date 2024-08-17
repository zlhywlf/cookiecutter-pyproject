"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib
from typing import Any, Dict, Optional, Union


class Result:
    """Holds the captured result of the cookiecutter project generation."""

    def __init__(
        self,
        exception: Optional[Union[Exception, SystemExit]],
        exit_code: Optional[Union[str, int]],
        project_dir: Optional[str],
        context: Optional[Dict[str, Any]],
    ) -> None:
        """Init."""
        self.exception = exception
        self.exit_code = exit_code
        self.context = context
        self._project_dir = project_dir

    @property
    def project_path(self) -> Optional[pathlib.Path]:
        """Return a pathlib.Path object if no exception occurred."""
        if self.exception is None and self._project_dir:
            return pathlib.Path(self._project_dir)
        return None
