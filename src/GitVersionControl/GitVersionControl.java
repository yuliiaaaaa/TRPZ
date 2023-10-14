package GitVersionControl;

import java.sql.Connection;
import java.util.Date;

import Repositories.CommitRepository;
import Services.CommitService;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.storage.file.FileRepositoryBuilder;
import org.eclipse.jgit.revwalk.RevCommit;

import java.io.File;
import java.io.IOException;

public class GitVersionControl implements IVersionControlSystem {
    private Connection connection;

    public GitVersionControl(Connection connection) {
        this.connection = connection;
    }

    private Repository initGitRepository(String repoDirectory) throws IOException {
        return new FileRepositoryBuilder()
                .setGitDir(new File(repoDirectory + "/.git"))
                .readEnvironment() // Consider environment variables
                .findGitDir()
                .build();
    }

    public void add(String repoName, String fileName) {
        String repoDirectory = "D:\\ТПРЗ\\" + repoName;

        try {
            // Initialize the Git repository using JGit
            Repository repository = initGitRepository(repoDirectory);
            Git git = new Git(repository);
            git.add().addFilepattern(fileName).call();

            git.close();
        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }

    public void commit(String repoName, String fileName, int repoId, String message, Date commitDate) {
        String repoDirectory = "D:\\ТПРЗ\\" + repoName;

        // Check if there are tracked files in the repository
        if (!hasTrackedFiles(repoDirectory)) {
            System.out.println("No tracked files in the repository.");
            return;
        }

        try {
            // Initialize the Git repository using JGit
            Repository repository = initGitRepository(repoDirectory);
            Git git = new Git(repository);
            git.commit().setMessage(message).call();
            git.close();
            CommitService commitService = new CommitService(new CommitRepository(connection));
            commitService.storeCommitInformation(repoId, message, commitDate);
        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void watchHistory(String repoName) {
        String repoDirectory = "D:\\ТПРЗ\\" + repoName;

        try {
            Repository repository = new FileRepositoryBuilder()
                    .setGitDir(new File(repoDirectory + "/.git"))
                    .readEnvironment()
                    .findGitDir()
                    .build();

            Git git = new Git(repository);


            Iterable<RevCommit> commits = git.log().call();

            System.out.println("Commit History for " + repoName + ":");
            for (RevCommit commit : commits) {
                String commitHash = commit.getId().getName();
                System.out.println(commit.getFullMessage()+ " " +commitHash);
            }

            printCommitHistory(repoDirectory);
            git.close();
        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }

    public void initializeRepository(String repoDirectory) {
        File gitDir = new File(repoDirectory + "/.git");
        if (gitDir.exists() && gitDir.isDirectory()) {
            System.out.println("Git repository already exists in: " + repoDirectory);
        } else {
            try {
                // Create a ProcessBuilder for the git init command
                Repository repository = FileRepositoryBuilder.create(new File(repoDirectory + "/.git"));
                repository.create();
                System.out.println("Git repository initialized successfully in: " + repoDirectory);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void printCommitHistory(String repoDirectory) {
        String gitExecutablePath = "C:\\Program Files\\Git\\cmd\\git.exe"; // Use the appropriate path
        String[] gitCommand = {gitExecutablePath, "log", "--graph","--all","--decorate"};

        ProcessBuilder processBuilder = new ProcessBuilder(gitCommand)
                .directory(new File(repoDirectory))
                .redirectOutput(ProcessBuilder.Redirect.INHERIT)
                .redirectError(ProcessBuilder.Redirect.INHERIT);

        try {
            Process process = processBuilder.start();
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.err.println("Git command failed with exit code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    private boolean hasTrackedFiles(String repoDirectory) {
        try {
            // Initialize the Git repository using JGit
            Repository repository = initGitRepository(repoDirectory);
            Git git = new Git(repository);
            return !git.status().call().getUntracked().isEmpty();
        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
        return false;
    }


}


