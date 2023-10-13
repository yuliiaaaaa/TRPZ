package Entities;


import java.util.Date;

public class CommitDTO {
    private int id;
    private int repoId;
    private String message;
    private final Date commitDate;

    public CommitDTO(int id, int repoId, String message, Date commitDate) {
        this.id = id;
        this.repoId = repoId;
        this.message = message;
        this.commitDate = commitDate;
    }

    public int getId() {
        return id;
    }

    public int getRepoId() {
        return repoId;
    }

    public String getMessage() {
        return message;
    }

    public void setId(int generatedId) {
    }

    public Date getCommitDate() {
        return commitDate;
    }
}
