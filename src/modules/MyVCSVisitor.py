from src.modules.VCSVisitor import VCSVisitor


class MyVCSVisitor(VCSVisitor):
    def visit_git(self, git_vc):
        return git_vc.show_repositories()

    def visit_mercurial(self, mercurial_vc):
       return mercurial_vc.show_repositories()

    def visit_svn(self, svn_vc):
       return svn_vc.show_repositories()