"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib
import subprocess  # noqa: S404
import sys
from datetime import datetime, timedelta, timezone
from typing import List

import pkg_resources  # type: ignore
from pydantic import BaseModel, Field, computed_field


def get_dev_dependencies() -> List[str]:
    """Dev dependencies."""
    dev_dependencies = ["ruff", "pytest", "faker", "mypy", "build", "pre-commit", "pytest-cov", "pytest-env"]
    dev_dependencies.sort()
    subprocess.check_call(  # noqa:  S603
        ["pip3", "install", "-i", "https://mirrors.aliyun.com/pypi/simple", *dev_dependencies]  # noqa:  S607
    )
    return get_dependency_versions(*dev_dependencies)


class Context(BaseModel):
    """cookiecutter context."""

    project_name: str = f'Python Project {datetime.now(tz=timezone(timedelta(hours=8))).strftime("%Y%m%d%H%M%S")}'
    project_slug: str = "{{ cookiecutter.project_name.lower().replace(' ', '_') }}"
    author: str = "Anonymous"
    email: str = "Anonymous"
    description: str = "The {{ cookiecutter.project_name }} application."
    dev_dependencies: List[str] = Field(default_factory=get_dev_dependencies, serialization_alias="__dev_dependencies")

    @computed_field(alias="__py_version")
    def py_version(self) -> str:
        """The version of python."""
        return f"{sys.version_info.major}.{sys.version_info.minor}"

    @computed_field(alias="__ruff_version")
    def ruff_version(self) -> str:
        """The version of ruff."""
        for _ in self.dev_dependencies:
            if "ruff" in _:
                return str(_)
        return "ruff"


def modify_last_digit(version: str) -> str:
    """Modify the last digit of the version number to 0."""
    parts = version.split(".")
    if len(parts) == 3 and parts[-1].isdigit():
        parts[-1] = "0"
        return "~=" + ".".join(parts)
    return "==" + version


def get_dependency_versions(*dependencies: str) -> List[str]:
    """Get dependency versions."""
    versions = []
    for dependency in dependencies:
        try:
            version = pkg_resources.get_distribution(dependency).version
            versions.append(f"{dependency}{modify_last_digit(version)}")
        except pkg_resources.DistributionNotFound:
            pass
    return versions


def generate_context() -> None:
    """Generate cookiecutter.json."""
    context = Context()
    with pathlib.Path("cookiecutter.json").open("w") as file:
        file.write(context.model_dump_json(by_alias=True))


def main() -> None:
    """Pre prompt hook."""
    generate_context()


if __name__ == "__main__":
    main()
