import pytest
from app.models import Status

@pytest.fixture
def get_status_enum():
    return Status
