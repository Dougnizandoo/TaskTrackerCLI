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
    if not function_status:
        assert msg == 'The entry must contain 5 keys!'

def test_read_data_all(get_data_writer):
    sample_data = [
        {'id': 1, 'description': 'Note 1', 'status': 1, 'created_at': '2025-06-25 10:00:00', 'updated_at': '2025-06-25 10:00:00'},
        {'id': 2, 'description': 'Note 2', 'status': 2, 'created_at': '2025-06-25 10:20:00', 'updated_at': '2025-06-25 10:20:00'},
        {'id': 3, 'description': 'Note 3', 'status': 3, 'created_at': '2025-06-25 12:00:00', 'updated_at': '2025-06-25 12:00:00'},
    ]
    for entry in sample_data:
        get_data_writer.insert_data(entry)

    status, data_load = get_data_writer.read_data()
    assert status is True
    assert len(data_load) == 3
    assert all(isinstance(item, dict) and len(item) == 5 for item in data_load)

@pytest.mark.parametrize('status_code, expected_count', [
    (1, 1),
    (2, 1),
    (3, 1)
])
def test_read_data_filter(get_data_writer, status_code, expected_count):
    sample_data = [
        {'id': 1, 'description': 'Note 1', 'status': 1, 'created_at': '...', 'updated_at': '...'},
        {'id': 2, 'description': 'Note 2', 'status': 2, 'created_at': '...', 'updated_at': '...'},
        {'id': 3, 'description': 'Note 3', 'status': 3, 'created_at': '...', 'updated_at': '...'}
    ]
    for entry in sample_data:
        get_data_writer.insert_data(entry)

    ok, filtered = get_data_writer.read_data(status_code)
    assert ok is True
    assert isinstance(filtered, list)
    assert len(filtered) == expected_count

@pytest.mark.parametrize('data_test, function_status', [
    ({'id': 1, 'description': 'Updated 1', 'status': 1, 'created_at': '...', 'updated_at': '...'}, False),
    ({'id': 2, 'description': 'Updated 2', 'status': 2, 'created_at': '...', 'updated_at': '...'}, True)
])
def test_update_data(get_data_writer, data_test, function_status):
    valid_entry = {'id': 2, 'description': 'Original', 'status': 2, 'created_at': '...', 'updated_at': '...'}
    get_data_writer.insert_data(valid_entry)

    ok, msg = get_data_writer.update_data(data_test)
    assert ok == function_status
    if not function_status:
        assert msg == 'ID not found!'

@pytest.mark.parametrize('initial_ids, delete_id, expected_result, expected_remaining_ids', [
    ([1, 2, 3], 2, True, [1, 2]),
    ([1, 2], 3, False, [1, 2])
])
def test_delete_data(get_data_writer, initial_ids, delete_id, expected_result, expected_remaining_ids):
    for idx in initial_ids:
        get_data_writer.insert_data({
            'id': idx,
            'description': f'Note {idx}',
            'status': 1,
            'created_at': '...',
            'updated_at': '...'
        })

    ok, msg = get_data_writer.delete_data(delete_id)
    assert ok == expected_result

    if ok:
        _, remaining = get_data_writer.read_data()
        assert [item['id'] for item in remaining] == expected_remaining_ids
    else:
        assert msg == 'ID not found!'
