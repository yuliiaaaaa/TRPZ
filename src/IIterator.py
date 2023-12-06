from abc import ABC, abstractmethod

class RepositoryIteratorInterface(ABC):
    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def isDone(self):
        pass

    @abstractmethod
    def currentItem(self):
        pass
