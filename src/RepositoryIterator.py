from IIterator import RepositoryIteratorInterface

class RepositoryIterator(RepositoryIteratorInterface):
    def __init__(self, repositories):
        self.repositories = repositories
        self.index = 0

    def first(self):
        self.index = 0

    def next(self):
        self.index += 1

    def isDone(self):
        return self.index >= len(self.repositories)

    def currentItem(self):
        if self.isDone():
            return None
        return self.repositories[self.index]

    def __iter__(self):
        return self

    def __next__(self):
        if self.isDone():
            raise StopIteration
        item = self.currentItem()
        self.next()
        return item
