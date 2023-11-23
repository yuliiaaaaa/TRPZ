from abc import ABC, abstractmethod
from typing import List

class IRepository(ABC):
    @abstractmethod
    def findById(self, id: int):
        pass

    @abstractmethod
    def findAll(self) -> List:
        pass

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass
