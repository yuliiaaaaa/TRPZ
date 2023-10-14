package Entities;

public class BranchDTO {
    private int id;
    private int repoId;
    private String name;

    public BranchDTO(int id, int repoId, String name) {
        this.id = id;
        this.repoId =repoId;
        this.name =name;
    }
}

