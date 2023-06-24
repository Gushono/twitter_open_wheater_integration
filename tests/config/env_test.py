import os

import pytest

from src.config.env import validate_environment_variables, REQUIRED_ENV_VARIABLES


@pytest.fixture()
def clean_environment_variables():
    for var in REQUIRED_ENV_VARIABLES:
        os.environ.pop(var, None)


def test_validate_environment_variables_all_variables_present(clean_environment_variables):
    for var in REQUIRED_ENV_VARIABLES:
        os.environ[var] = "value"

    validate_environment_variables()


def test_validate_environment_variables_missing_variables(clean_environment_variables):
    with pytest.raises(Exception) as ex:
        validate_environment_variables()

    missing_variables = ex.value.args[0]
    assert all(var in missing_variables for var in REQUIRED_ENV_VARIABLES)
