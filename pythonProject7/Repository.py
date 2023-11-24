import os

import psycopg2
from git import Repo

from RepositoryDTO import RepositoryDTO
from RepositoryIterator import RepositoryIterator


class Repository:
    def __init__(self, connection):
        self.connection = connection

    def find_by_id(self, id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM vcsrepositories WHERE id = %s", (id,))
            result = cursor.fetchone()

            if result:
                repo_id, name, vcs_type, url = result
                return RepositoryDTO(repo_id, name, vcs_type, url)
        except (psycopg2.Error, Exception) as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

        return None

    def find_all(self):
        repositories = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM vcsrepositories")
            results = cursor.fetchall()

            for result in results:
                repo_id, name, vcs_type, url = result
                repositories.append(RepositoryDTO(repo_id, name, vcs_type, url))
        except (psycopg2.Error, Exception) as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

        return repositories

    def initialize_repository(self, repo_directory, repo_name, vcs_type, url):
        git_dir = os.path.join(repo_directory, ".git")
        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            print(f"Git repository already exists in: {repo_directory}")
            self.repo = Repo(repo_directory)  # Initialize the Git repository
        else:
            try:
                self.repo = Repo.init(repo_directory)  # Initialize the Git repository
                print(f"Git repository initialized successfully in: {repo_directory}")
                # Insert repository details into the database using the existing Repository class
                repository = Repository(self.connection)
                repository.create(RepositoryDTO(None, repo_name, vcs_type, url))
            except Exception as e:
                print(f"Error initializing Git repository: {e}")

    def create(self, entity):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO vcsrepositories(name, vcs_type, url) VALUES (%s, %s, %s)", (entity.name, entity.vcs_type, entity.url))
            self.connection.commit()
        except (psycopg2.Error, Exception) as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def update(self, entity):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE vcsrepositories SET name = %s, vcs_type = %s, url = %s WHERE id = %s", (entity.name, entity.vcs_type, entity.url, entity.id))
            self.connection.commit()
        except (psycopg2.Error, Exception) as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def delete(self, id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM vcsrepositories WHERE id = %s", (id,))
            self.connection.commit()
        except (psycopg2.Error, Exception) as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
