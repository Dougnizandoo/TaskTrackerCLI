import pytest
from app.models import Status
from app.models import Task


@pytest.fixture
def get_status_enum():
    return Status

@pytest.fixture
def get_task_model():
    model = Task(id=1, description='Test note', created_at='2025-06-25 18:00:00', updated_at='2025-06-25 18:20:00')
    return model
