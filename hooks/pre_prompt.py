from __future__ import annotations

import json
import pathlib
import subprocess  # noqa: S404
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

import pkg_resources  # type: ignore[import]

VERSION_PART = 3
DEV_DEPENDENCIES = [
    "ruff",
    "pytest",
    "faker",
    "mypy",
    "build",
    "pre-commit",
    "pytest-cov",
    "pytest-env",
    "pytest-mock",
]


@dataclass
class Context:
    """cookiecutter context."""

    project_name: str = f"Python Project {datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y%m%d%H%M%S')}"
    project_slug: str = "{{ cookiecutter.project_name.lower().replace(' ', '_') }}"
    author: str = "Anonymous"
    email: str = "Anonymous"
    description: str = "The {{ cookiecutter.project_name }} application"


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


def get_dev_dependencies() -> dict[str, str]:
    """Get dependency versions.

    Returns:
        list
    """
    subprocess.check_call(  # noqa:  S603
        ["pip3", "install", "-i", "https://mirrors.aliyun.com/pypi/simple", *DEV_DEPENDENCIES],  # noqa:  S607
    )
    versions = {}
    try:
        for dependency in DEV_DEPENDENCIES:
            version = pkg_resources.get_distribution(dependency).version
            versions[dependency] = f"{dependency}{modify_last_digit(version)}"
    except pkg_resources.DistributionNotFound:
        pass
    return versions


def private_context() -> dict[str, str | list[str]]:
    """Private context.

    Returns:
        dict
    """
    dev_dependencies = get_dev_dependencies()
    return {
        "__py_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "__dev_dependencies": sorted(dev_dependencies.values()),
        "__ruff_version": dev_dependencies.get("ruff", "ruff"),
    }


def main() -> None:
    """Pre prompt hook."""
    context = Context()
    with pathlib.Path("cookiecutter.json").open("w", encoding="utf-8") as file:
        json.dump({**asdict(context), **private_context()}, file)


if __name__ == "__main__":
    main()
