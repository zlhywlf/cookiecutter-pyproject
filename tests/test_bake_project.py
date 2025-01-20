from faker import Faker

from hooks.pre_prompt import Context
from tests.core import Baker


def test_bake_project(baker: Baker, faker: Faker) -> None:
    """Test bake project."""
    context = Context(project_name=faker.name())
    result = baker.bake(context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir
