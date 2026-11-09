from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id, full_name, email):
        self.__person_id = person_id
        self.__full_name = full_name
        self.__email = email

    @property
    def person_id(self):
        return self.__person_id

    @property
    def full_name(self):
        return self.__full_name

    @property
    def email(self):
        return self.__email

    @abstractmethod
    def display_details(self):
        pass