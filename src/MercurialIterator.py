from typing import List
from IIterator import RepositoryIteratorInterface
from RepositoryDTO import RepositoryDTO


class MercurialRepositoryIterator(RepositoryIteratorInterface):
    def __init__(self, repositories: List[RepositoryDTO]):
        self.repositories = [repo for repo in repositories if repo.vcs_type == "Mercurial"]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> RepositoryDTO:
        if self.isDone():
            raise StopIteration("Reached end of the collection")
        repo = self.repositories[self.index]
        self.index += 1
        return repo

    def first(self):
        if len(self.repositories) > 0:
            self.index = 0  # Set the index to the beginning of the collection
        else:
            raise ValueError("Collection is empty")

    def next(self) -> RepositoryDTO:
        if self.isDone():
            raise StopIteration("Reached end of the collection")
        repo = self.repositories[self.index]
        self.index += 1
        return repo

    def isDone(self) -> bool:
        return self.index >= len(self.repositories)

    def currentItem(self) -> RepositoryDTO:
        if self.isDone():
            raise ValueError("Iterator is at the end, no current item available")
        return self.repositories[self.index]

