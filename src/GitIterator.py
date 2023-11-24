from typing import List
from IIterator import RepositoryIteratorInterface
from RepositoryDTO import RepositoryDTO


class GitRepositoryIterator(RepositoryIteratorInterface):
    def __init__(self, repositories: List[RepositoryDTO]):
        self.repositories = [repo for repo in repositories if repo.vcs_type == "Git"]
        self.index = 0


    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.repositories):
            raise StopIteration
        repo = self.repositories[self.index]
        self.index += 1
        return repo

    def first(self):
        if len(self.repositories) > 0:
            self.index = 0  # Set the index to the beginning of the collection
        else:
            raise ValueError("Collection is empty")

    def next(self):
        if self.isDone():
            raise StopIteration("Reached end of the collection")
        repo = self.repositories[self.index]
        self.index += 1
        return repo

    def isDone(self):
        return self.index >= len(self.repositories)

    def currentItem(self):
        if self.isDone():
            raise ValueError("Iterator is at the end, no current item available")
        return self.repositories[self.index]

