import pytest
from app.services import DataWriter


@pytest.fixture
def get_data_writer():
    return DataWriter('data_test_file.json')