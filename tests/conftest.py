import pathlib
from typing import Any, Generator

import py
import pytest
import yaml
from faker import Faker
from pytest_mock import MockerFixture

from tests.core import Baker, run_script


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Create and return a session-scoped Faker instance.

    This fixture provides a Faker instance that is shared across the entire test session.
    Using a session scope ensures that the Faker instance is created only once, improving test efficiency.

    Returns:
        Faker: An instance of Faker for generating fake data.
    """
    return Faker()


@pytest.fixture(scope="session")
def config_path(tmpdir_factory: pytest.TempdirFactory) -> py.path.local:
    """Create and return a configuration file path for the test session.

    This fixture sets up a temporary user directory containing a `config.yaml` file.
    The configuration file includes paths to directories used for storing cookiecutters and replay data.

    Args:
        tmpdir_factory: A pytest fixture that provides a temporary directory factory.

    Returns:
        py.path.local: Path to the created `config.yaml` file.
    """
    user_dir = tmpdir_factory.mktemp("user_dir")
    config = user_dir.join(pathlib.Path("config.yaml"))
    with config.open("w", encoding="utf-8") as f:
        yaml.dump(
            {
                "cookiecutters_dir": user_dir.mkdir("cookiecutters").strpath,
                "replay_dir": user_dir.mkdir("cookiecutter_replay").strpath,
            },
            f,
            Dumper=yaml.Dumper,
        )
    return config


@pytest.fixture
def baker(tmpdir: py.path.local, config_path: py.path.local, mocker: MockerFixture) -> Generator[Baker, Any, None]:
    """Create and return a Baker instance for testing purposes.

    This fixture sets up a `Baker` instance by mocking certain functions and creating temporary directories.
    It ensures that the `Baker` instance is properly initialized and cleaned up after use.

    Args:
        tmpdir: A pytest fixture providing a temporary directory.
        config_path: Path to the configuration file created by the `config_path` fixture.
        mocker: A pytest-mock fixture used to mock objects and methods.

    Yields:
        Baker: An instance of Baker configured with the provided parameters.

    Notes:
        - Mocks the `run_script` function in `cookiecutter.hooks`.
        - Mocks the `subprocess` module in `hooks.pre_prompt`.
        - Creates a temporary output directory named `cookies`.
        - Cleans up the temporary output directory after tests.
    """
    # Mock the run_script function in cookiecutter.hooks
    mocker.patch("cookiecutter.hooks.run_script", new=run_script)
    mocker.patch("hooks.pre_prompt.subprocess")
    output_path = tmpdir.mkdir("cookies")
    yield Baker(pathlib.Path(), output_path, config_path)
    output_path.remove()
