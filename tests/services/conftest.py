import pytest
from app.services import DataWriter


@pytest.fixture
def get_data_writer(tmp_path):
    test_file = tmp_path / "test_data.json"
    return DataWriter(data_file_name=str(test_file))
