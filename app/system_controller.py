from time import sleep
from app.models import Task as model, Status
from app.services import DataWriter as dw


class Controller():
    def __init__(self):
        self.__last_search = None
        self.__data_was_updated = False
        self.__choices = None
    
    # Create task
    def _add_data(self):
        print("Text your new note:")
        description = input("> ").strip()

        self.__choices = ('Save this task', 'cancel')
        user_choice = self._user_choice(hide_exite=True)

        if user_choice == 1:
            
            if self.__data_was_updated is True:
                self._update_last_search()

            next_id = len(self.__last_search) + 1 if len(self.__last_search) > 0 else 1
            new_task = model(id=next_id, description=description)

            ok, msg = dw().insert_data(new_task.to_dict())
            print(msg)
            if ok is True:
                self.__data_was_updated = ok

    # Read all tasks
    def _read_data(self, filter: int = 0):
        if self.__data_was_updated is False and self.__last_search is not None and filter == 0:
            saved_data = self.__last_search
        
        else:
            ok, saved_data = dw().read_data(filter)
            if ok is False:
                print(saved_data)
            
            if ok is True and filter == 0:
                self.__data_was_updated = False
                self.__last_search = saved_data
        
        if len(saved_data) == 0:
            print('Your task list is empty!')
        else:
            print('=' * 115)
            print(f"|{'YOUR REGISTRED TASKS!':^107}|")
            print('=' * 115)
            print(f'|{"ID":^5} | {"Description":<50} | {"Status":^10} | {"Created at":^18} | {"Updated at":^18}|')
            print('_' * 115)
            for item in saved_data:
                print(f'|{item.get('id'):^5} | {item.get('description'):<50} | {Status(item.get('status')).name:^10} | {item.get('created_at'):^18} | {item.get('updated_at'):^18}|')
                print('-' * 115)

    # Read filtered tasks
    def _filter_data(self):
        self.__choices = (Status.NOT_DONE.name, Status.IN_PROGRESS.name, Status.DONE.name)
        user_choice = self._user_choice()

        if isinstance(user_choice, int):
            self._read_data(user_choice)

    # Update a task
    def _update_data(self):
        if self.__data_was_updated is True or self.__last_search is None:
            self._update_data()
        
        if len(self.__last_search) == 0:
            print("You don't have any task registred!")
            return None

        print("What is the task ID that you wanna to update?")
        choosen_id = int(input("> "))
        if choosen_id > 0 and choosen_id <= len(self.__last_search):
            self.__choices = ("Description", "Status", "Both")
            print("\nWhat do you wanna to update?")
            user_choice = self._user_choice()

            if user_choice != 'e':
                
                for item in self.__last_search:
                    if item['id'] == choosen_id:
                        task_to_update = model(
                                            id=item['id'], description=item['description'],
                                            status=item['status'], created_at=item['created_at']
                                            )
                        break
                
                if user_choice == 1 or user_choice == 3:
                    print(f'The actual task is: "{task_to_update.description}"')
                    print("Now updated the task:")
                    updated_description = input("> ").strip()
                
                if user_choice == 2 or user_choice == 3:
                    print(f'The actual task status is: "{Status(task_to_update.status).name}"')
                    print("Now updated the task's status:")
                    self.__choices = (Status.NOT_DONE.name, Status.IN_PROGRESS.name, Status.DONE.name)
                    updated_status = self._user_choice(True)
                
                if user_choice == 1 or user_choice == 3:
                    print(f'Do you wanna save this updated description?\nnew description:"{updated_description}"')
                
                if user_choice == 2 or user_choice == 3:
                    print(f'Do you wanna save this updated status?\nnew task status:"{Status(updated_status).name}"')

                self.__choices = ('Save updated task', 'cancel')
                save_or_not = self._user_choice(hide_exite=True)

                if save_or_not == 1:
                    if user_choice == 1 or user_choice == 3:
                        task_to_update.description = updated_description
                    
                    if user_choice == 2 or user_choice == 3:
                        task_to_update.status = updated_status
                    
                    ok, msg = dw().update_data(task_to_update.to_dict())
                    print(msg)
                    if ok is True:
                        self.__data_was_updated = True

                else:
                    print('Canceling operation...')
                    sleep(1)

        else:
            print(f'ID not found!')

    # Delete a task
    def _delete_data(self):
        if self.__data_was_updated is True or self.__last_search is not None:
            self._update_last_search()
        
        if len(self.__last_search) == 0:
            print("You don't have any task registred!")
            return None
        
        choosen_id = int(input("> "))
        if choosen_id > 0 and choosen_id <= len(self.__last_search):
            choices = ("Delete this task", "Cancel operation")
            self.__choices = choices

            user_choice = self._user_choice(True)
            if user_choice == 1:
                ok, msg = dw().delete_data(choosen_id)
                print(msg)
                if ok is True:
                    self.__data_was_updated = True
            
            else:
                print('Canceling operation...')
                sleep(1)
            
        else:
            print(f'ID not found!')

    # main function
    def main(self):
        actions = {
                1: self._add_data,
                2: self._read_data,
                3: self._filter_data,
                4: self._update_data,
                5: self._delete_data
            }
        while True:
            self.__choices = (
                    'Create new task', 'See all tasks', 'Filter tasks',
                    'Update Task', 'Delete Task')
            user_choice = self._user_choice()
                
            if user_choice == 'e':
                print('Closing application...')
                sleep(2) 
                break
            print('')
            actions[user_choice]()
            print('')


    # ----------------- helper --------------------
    # make the user choose one
    def _user_choice(self,hide_exite: bool = False) -> str | int:
        # Choice Validation
        while True:
            for index, choice in enumerate(self.__choices):
                print(f'[ {index + 1} ] - {choice};')
            if hide_exite is False:
                print(f'[ e ] - Exit;\n')
            
            user_choice = input("> ").strip()

            if user_choice.lower() == 'e':
                user_choice = user_choice.lower()
                break

            if user_choice.isdigit() and 1 <= int(user_choice) <= len(self.__choices):
                user_choice = int(user_choice)
                break
            else:
                if hide_exite is not True:
                    print(f"\nInvalid option! Please enter a number between 1 and {len(self.__choices)} or 'E' to exit.\n")
                else:
                    print(f"\nInvalid option! Please enter a number between 1 and {len(self.__choices)}")
        return user_choice
    
    # Count data
    def _update_last_search(self):
        ok, data = dw().read_data()
        if not ok:
            print(data)
        else:
            self.__last_search = data
            self.__data_was_updated = False