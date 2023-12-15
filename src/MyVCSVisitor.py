from src.VCSVisitor import VCSVisitor


class MyVCSVisitor(VCSVisitor):
    def visit_git(self, git_vc):
        git_vc.show_repositories()

    def visit_mercurial(self, mercurial_vc):
        mercurial_vc.show_repositories()

    def visit_svn(self, svn_vc):
        svn_vc.show_repositories()