"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker

from tests.model.Context import Context
from tests.model.Cookies import Cookies


def test_bake_project(cookies: Cookies, faker: Faker) -> None:
    """Test bake project."""
    name = faker.name()
    slug = name.lower().replace(" ", "_")
    result = cookies.bake(extra_context={"project_name": name})
    context = Context.model_validate(result.context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path
    assert result.project_path.name == slug
    assert result.project_path.is_dir()
    assert context.project_slug == slug
    assert context.author == "Anonymous"
    assert context.project_name == name
