import pytest


@pytest.mark.parametrize('data_test, function_status', [
    ({'id': 1, 'description': 'Test note 1','status': 1, 'created_at': '2025-06-25 10:00:00', 'updated_at': '2025-06-25 10:00:00'}, True),
    ({'id': 2, 'description': 'Test note 2','status': 2, 'created_at': '2025-06-25 10:20:00', 'updated_at': '2025-06-25 10:20:00'}, True),
    ({'id': 3, 'description': 'Test note 3','status': 1, 'created_at': '2025-06-25 12:00:00'}, False),
    ({'id': 4, 'description': 'Test note 4','status': 3, 'created_at': '2025-06-25 19:00:00', 'updated_at': '2025-06-25 19:00:00'}, True)
])
def test_insert_data(get_data_writer, data_test, function_status):
    ok, msg = get_data_writer.insert_data(data_test)
    assert ok == function_status
    if function_status == False:
        assert msg == 'The entry must contain 5 keys!'


def test_read_data_all(get_data_writer):
    status, data_load = get_data_writer.read_data()
    assert status is True
    assert len(data_load) == 3
    assert isinstance(data_load, list)
    for item in data_load:
        assert isinstance(item, dict)
        assert len(item) == 5


@pytest.mark.parametrize('status_code, how_many_expected, found_search', [
    (1, 1, True),
    (2, 1, True),
    (3, 1, True),
])
def test_read_data_filter(get_data_writer, status_code, how_many_expected, found_search):
    ok, data_search = get_data_writer.read_data(status_code)
    assert ok == found_search
    assert isinstance(data_search, list)
    assert len(data_search) == how_many_expected


@pytest.mark.parametrize('data_test, function_status', [
    ({'id': 1, 'description': 'michael jordan 23','status': 3, 'created_at': '2025-06-25 10:00:00', 'updated_at': '2025-06-25 23:23:23'}, True),
    ({'id': 2, 'description': 'robsu 777','status': 2, 'created_at': '2025-06-25 10:20:00', 'updated_at': '2025-06-25 19:25:00'}, True),
    ({'id': 3, 'description': 'Test note 3','status': 1, 'created_at': '2025-06-25 12:00:00', 'updated_at': '2025-06-25 19:25:00'}, False),
    ({'id': 4, 'description': 'asking alexandria','status': 3, 'created_at': '2025-06-25 19:00:00', 'updated_at': '2025-06-26 00:22:12'}, True)
])
def test_update_data(get_data_writer, data_test, function_status):
    ok, msg = get_data_writer.update_data(data_test)
    assert ok == function_status
    if function_status is False:
        assert msg == 'ID not found!'


@pytest.mark.parametrize('id_for_test, expected', [
    (1, True),
    (2, True),
    (3, False),
    (1, True)
])
def test_delete_data(get_data_writer, id_for_test, expected):
    ok, msg = get_data_writer.delete_data(id_for_test)
    assert ok == expected
    if expected is False:
        assert msg == 'ID not found!'