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
    """Get data faker.

    Returns:
        Faker
    """
    return Faker()


@pytest.fixture(scope="session")
def config_path(tmpdir_factory: pytest.TempdirFactory) -> py.path.local:
    """Generate cookiecutter configuration file.

    Returns:
        local
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
    """Yield an instance of the Cookies helper class that can be used to generate a project from a template."""
    mocker.patch("cookiecutter.hooks.run_script", new=run_script)
    mocker.patch("hooks.pre_prompt.subprocess")
    output_path = tmpdir.mkdir("cookies")
    yield Baker(pathlib.Path(), output_path, config_path)
    output_path.remove()
