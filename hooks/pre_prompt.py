from __future__ import annotations

import json
import pathlib
import subprocess  # noqa: S404
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

import pkg_resources  # type: ignore[import]


def get_dev_dependencies() -> list[str]:
    """Dev dependencies.

    Returns:
        list
    """
    dev_dependencies = ["ruff", "pytest", "faker", "mypy", "build", "pre-commit", "pytest-cov", "pytest-env", "pytest-mock"]
    dev_dependencies.sort()
    subprocess.check_call(  # noqa:  S603
        ["pip3", "install", "-i", "https://mirrors.aliyun.com/pypi/simple", *dev_dependencies],  # noqa:  S607
    )
    return get_dependency_versions(*dev_dependencies)


@dataclass
class Context:
    """cookiecutter context."""

    project_name: str = f"Python Project {datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y%m%d%H%M%S')}"
    project_slug: str = "{{ cookiecutter.project_name.lower().replace(' ', '_') }}"
    author: str = "Anonymous"
    email: str = "Anonymous"
    description: str = "The {{ cookiecutter.project_name }} application"


VERSION_PART = 3


def modify_last_digit(version: str) -> str:
    """Modify the last digit of the version number to 0.

    Returns:
        str
    """
    parts = version.split(".")
    if len(parts) == VERSION_PART and parts[-1].isdigit():
        parts[-1] = "0"
        return "~=" + ".".join(parts)
    return "==" + version


def get_dependency_versions(*dependencies: str) -> list[str]:
    """Get dependency versions.

    Returns:
        list
    """
    versions = []
    try:
        for dependency in dependencies:
            version = pkg_resources.get_distribution(dependency).version
            versions.append(f"{dependency}{modify_last_digit(version)}")
    except pkg_resources.DistributionNotFound:
        pass
    return versions


def generate_context() -> None:
    """Generate cookiecutter.json."""
    context = Context()
    dev_dependencies = get_dev_dependencies()
    ruff_version = "ruff"
    for _ in dev_dependencies:
        if "ruff" in _:
            ruff_version = _
            break
    with pathlib.Path("cookiecutter.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                **asdict(context),
                "__py_version": f"{sys.version_info.major}.{sys.version_info.minor}",
                "__dev_dependencies": dev_dependencies,
                "__ruff_version": ruff_version,
            },
            file,
        )


def main() -> None:
    """Pre prompt hook."""
    generate_context()


if __name__ == "__main__":
    main()
