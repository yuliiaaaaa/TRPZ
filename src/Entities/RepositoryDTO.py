class RepositoryDTO:
    def __init__(self, id, name, vcs_type, url):
        self.id = id
        self.name = name
        self.vcs_type = vcs_type
        self.url = url

    def __str__(self):
        return f"RepositoryDTO(id={self.id}, name={self.name}, type={self.type}, url={self.url})"
