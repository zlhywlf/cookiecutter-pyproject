from __future__ import annotations

import pathlib


class Result:
    """Holds the captured result of the cookiecutter project generation."""

    def __init__(
        self,
        exception: Exception | SystemExit | None,
        exit_code: str | int | None,
        project_dir: str | None,
    ) -> None:
        """Init."""
        self.exception = exception
        self.exit_code = exit_code
        self._project_dir = project_dir

    @property
    def project_path(self) -> pathlib.Path | None:
        """Return a pathlib.Path object if no exception occurred."""
        if self.exception is None and self._project_dir:
            return pathlib.Path(self._project_dir)
        return None
