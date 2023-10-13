package Repositories;

import Entities.CommitDTO;

import java.util.List;

public interface ICommitRepository {
    CommitDTO findByIdCommit(int id);
    List<CommitDTO> findByRepoId(int repoId);
    void createCommit(CommitDTO commit);
    void updateCommit(CommitDTO commit);
    void deleteCommit(int id);
    List<CommitDTO> findAllCommits();
}
