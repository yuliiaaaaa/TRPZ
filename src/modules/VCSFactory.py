from src.vcs.GitVersionControl import GitVersionControl
from src.vcs.MercurialVersionControl import MercurialVersionControl
from src.vcs.SVNVersionControl import SVNVersionControl


class VersionControlFactory:
    @staticmethod
    def create_version_control_system(connection, vcs_type):
        if vcs_type == "Git":
            return GitVersionControl(connection)
        elif vcs_type == "Mercurial":
            return MercurialVersionControl(connection)
        elif vcs_type == "SVN":
            return SVNVersionControl(connection)
        else:
            raise ValueError(f"Unsupported VCS type: {vcs_type}")