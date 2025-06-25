import pytest


@pytest.mark.parametrize('name, value', [
    ('NOT_DONE', 1),
    ('IN_PROGRESS', 2),
    ('DONE', 3)
])
def test_status_enum_values(get_status_enum, name, value):
    status_member = getattr(get_status_enum, name)
    assert status_member.value == value


@pytest.mark.parametrize('value, name', [
    (1, 'NOT_DONE'),
    (2, 'IN_PROGRESS'),
    (3, 'DONE')
])
def test_status_enum_names(get_status_enum, value, name):
    status_member = get_status_enum(value=value)
    assert status_member.name == name
