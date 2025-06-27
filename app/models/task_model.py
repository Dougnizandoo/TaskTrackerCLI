from datetime import datetime


class Task:
    def __init__(self, id: int, description: str, 
                status: int = 1,
                created_at: datetime = None,
                updated_at: datetime = None):
        self.__id = id
        self.__description = description
        self.__status = status
        self.__created_at = created_at or datetime.now().strftime('%m/%d/%Y - %H:%M')
        self.__updated_at = updated_at or datetime.now().strftime('%m/%d/%Y - %H:%M')

    def __str__(self):
        return f'Task number: {self.id}'

    # Get
    @property
    def id(self):
        return self.__id
    
    @property
    def description(self):
        return self.__description
    
    @property
    def status(self):
        return self.__status
    
    @property
    def created_at(self):
        return self.__created_at
    
    @property
    def updated_at(self):
        return self.__updated_at

    # Setters
    @description.setter
    def description(self, new_description):
        self.__description = new_description
        self.__updated_at = datetime.now().strftime('%m/%d/%Y - %H:%M')

    @status.setter
    def status(self, new_status: int):
        self.__status = new_status
        self.__updated_at = datetime.now().strftime('%m/%d/%Y - %H:%M')


    # dict model for saving
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
