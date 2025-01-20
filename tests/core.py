from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    """result."""

    exception: Exception | SystemExit | None = None
    exit_code: str | int | None = None
    project_dir: str | None = None


class Baker:
    """baker."""

    def bake(self, context: object) -> Result:
        """Generate project files.

        Returns:
            Result
        """
