# tests/conftest.py
import pytest
from application import application

@pytest.fixture(scope='module')
def test_client():
    with application.test_client() as testing_client:
        with application.app_context():
            yield testing_client