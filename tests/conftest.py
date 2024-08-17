"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pathlib
from typing import Any, Generator

import py
import pytest
import yaml
from faker import Faker

from tests.model.Cookies import Cookies


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Get data faker."""
    return Faker()


@pytest.fixture(scope="session")
def config_file(tmpdir_factory: pytest.TempdirFactory) -> py.path.local:
    """Generate cookiecutter configuration file."""
    user_dir = tmpdir_factory.mktemp("user_dir")
    config_file = user_dir.join(pathlib.Path("config"))
    config = {
        "cookiecutters_dir": str(user_dir.mkdir("cookiecutters")),
        "replay_dir": str(user_dir.mkdir("cookiecutter_replay")),
    }
    with config_file.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, Dumper=yaml.Dumper)
    return config_file


@pytest.fixture
def cookies(tmpdir: py.path.local, config_file: py.path.local) -> Generator[Cookies, Any, None]:
    """Yield an instance of the Cookies helper class that can be used to generate a project from a template."""
    output_dir = tmpdir.mkdir("cookies")
    output_factory = output_dir.mkdir
    yield Cookies(str(pathlib.Path().absolute()), output_factory, config_file)
    output_dir.remove()
