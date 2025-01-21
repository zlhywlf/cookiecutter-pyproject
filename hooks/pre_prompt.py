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
    """A data class to store project context information."""

    project_name: str = f"Python Project {datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y%m%d%H%M%S')}"
    project_slug: str = "{{ cookiecutter.project_name.lower().replace(' ', '_') }}"
    author: str = "Anonymous"
    email: str = "Anonymous"
    description: str = "The {{ cookiecutter.project_name }} application"


def modify_last_digit(version: str) -> str:
    """Modify the last digit of the version string according to specific rules.

    If the last part of the version string is a digit
    and the entire version number consists of the expected number of parts,
    replace the last part with '0' and prepend '~=' to the version number to indicate compatibility.
    If the conditions are not met, prepend '==' to the version number to indicate an exact match.

    Parameters:
    version (str): The version string to be modified.

    Returns:
    str: The modified version expression.
    """
    parts = version.split(".")
    if len(parts) == VERSION_PART and parts[-1].isdigit():
        parts[-1] = "0"
        return "~=" + ".".join(parts)
    return "==" + version


def get_dev_dependencies() -> dict[str, str]:
    """Install development dependencies and retrieve their version information.

    This function installs predefined development dependencies using subprocess,
    then retrieves the version information of these dependencies using pkg_resources.
    If a DistributionNotFound exception is encountered while retrieving the dependency version,
    it will be ignored, and the function will continue processing other dependencies.

    Returns:
        A dictionary where keys are dependency names and values are version strings of the dependencies.
        If a dependency is not found or its version cannot be retrieved, it will not be included in the result.
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
    """Generates and returns a dictionary containing private context information.

    Returns:
        A dictionary with the following keys:
        - "__py_version": A string representing the Python version in the format "major.minor".
        - "__dev_dependencies": A sorted list of strings representing development dependencies.
        - "__ruff_version": A string representing the version of the 'ruff' dependency, or "ruff" if not found.
    """
    dev_dependencies = get_dev_dependencies()
    return {
        "__py_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "__dev_dependencies": sorted(dev_dependencies.values()),
        "__ruff_version": dev_dependencies.get("ruff", "ruff"),
    }


def main() -> None:
    """Main function to export context information to a JSON file.

    This function creates a Context instance and writes its public and private attributes
    to the 'cookiecutter.json' file. It uses a with statement to ensure that the file
    operations are handled safely, even if an error occurs.
    """
    context = Context()
    with pathlib.Path("cookiecutter.json").open("w", encoding="utf-8") as file:
        json.dump({**asdict(context), **private_context()}, file)


if __name__ == "__main__":
    main()
