from abc import ABC, abstractmethod


class VCSVisitor(ABC):
    @abstractmethod
    def visit_git(self, git_vc):
        pass

    @abstractmethod
    def visit_mercurial(self, mercurial_vc):
        pass

    @abstractmethod
    def visit_svn(self, svn_vc):
        pass