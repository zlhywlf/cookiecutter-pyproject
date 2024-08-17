"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker

from hooks.pre_prompt import Context
from tests.model.Cookies import Cookies


def test_bake_project(cookies: Cookies, faker: Faker) -> None:
    """Test bake project."""
    context = Context(project_name=faker.name())
    result = cookies.bake(context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path
    assert result.project_path.name == context.project_slug
    assert result.project_path.is_dir()
