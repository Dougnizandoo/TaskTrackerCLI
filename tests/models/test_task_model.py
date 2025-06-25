import pytest


def test_model_attribute(get_task_model):
    assert get_task_model.id == 1
    assert get_task_model.description == 'Test note'
    assert get_task_model.status == 1
    assert get_task_model.created_at == '2025-06-25 18:00:00'
    assert get_task_model.updated_at == '2025-06-25 18:20:00'

def test_model_to_dict_keys(get_task_model):
    expected_dict = {'id', 'description', 'status', 'created_at', 'updated_at'}
    model_dict = get_task_model.to_dict()
    assert expected_dict.issubset(model_dict)

def test_model_to_dict_values(get_task_model):
    expected = {'id': 1, 'description': 'Test note',
                'status': 1, 'created_at': '2025-06-25 18:00:00',
                'updated_at': '2025-06-25 18:20:00'}
    model_dict = get_task_model.to_dict()
    for key in model_dict:
        assert model_dict[key] == expected[key]
