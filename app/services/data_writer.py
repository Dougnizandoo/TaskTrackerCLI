import os
import json
from pathlib import Path


script_dir = Path(__file__).parent
os.chdir(script_dir)


class DataWriter:
    def __init__(self, data_file_name = 'data.json'): # check if data exists
        self.__file = data_file_name
        if not os.path.exists(self.__file):
            create_json = self._write_data()
            if not create_json[0]:
                print(create_json[1])    

    # Helpers
    def _validate_entry(self, dict_to_validate: dict) -> tuple[bool, str]:
        expected_keys = {'id', 'description', 'status', 'created_at', 'updated_at'}
        if len(dict_to_validate) != 5:
            return False, "The entry must contain 5 keys!"

        if not expected_keys.issubset(dict_to_validate):
            return False, f'The dictionary must contain the following keys:\nkeys: {expected_keys}'
        return True, ""
    
    def _write_data(self, data_to_write: list = None) -> tuple[bool, str]:
        if data_to_write is None:
            data_to_write = []

        try:
            with open(self.__file, "w", encoding="utf-8") as f:
                json.dump(data_to_write, f, indent=4, ensure_ascii=False)
        except Exception as err:
            return False, f"Error!\nCouldn't save the data!\n{err}"
        return True, f'You saved your progress'

    # Create
    def insert_data(self, new_data: dict) -> tuple[bool, str]:
        ok, msg = self._validate_entry(new_data)
        if not ok:
            return ok, msg
        
        status, loaded_data = self.read_data()
        if not status:
            return status, loaded_data
        
        loaded_data.append(new_data)
        return self._write_data(loaded_data)

    # Read
    def read_data(self, status_filter: int = 0) -> tuple[bool, any]:
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
        except json.JSONDecodeError as err:
            return False, f'Error decoding JSON: {err}'
        except FileNotFoundError:
            return False, 'Data file not found.'
        except Exception as err:
            return False, f'Unexpected error: {err}'

        if status_filter == 0:
            return True, loaded_data

        elif status_filter in (1, 2, 3):
            filtered_list = []
            for index, item in enumerate(loaded_data):
                if item['status'] == status_filter:
                    filtered_list.append(item)
            return True, filtered_list

        else:
            return False, 'The status_filter number is invalid!'

    # Update
    def update_data(self, data_to_update: dict) -> tuple[bool, str]:
        ok, msg = self._validate_entry(data_to_update)
        if not ok:
            return ok, msg
        
        status, saved_data = self.read_data()
        if not status:
            return status, saved_data
        
        for index, item in enumerate(saved_data):
            if item.get('id') == data_to_update['id']:
                saved_data[index] = data_to_update
                break
        else:
            return False, 'ID not found!'
        
        return self._write_data(saved_data)

    # Delete
    def delete_data(self, data_id: int):
        status, saved_data = self.read_data()
        if not status:
            return status, saved_data
        
        for index, item in enumerate(saved_data):
            if item.get('id') == data_id:
                saved_data.pop(index)
                break

        else:
            return False, 'ID not found!'

        for new_id, item in enumerate(saved_data, start=1):
            item["id"] = new_id

        ok, msg = self._write_data(saved_data)
        if not ok:
            return ok, msg
        
        return ok, 'The task was deleted successfully!'
