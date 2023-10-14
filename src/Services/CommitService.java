package Services;

import Entities.CommitDTO;
import Repositories.ICommitRepository;

import java.util.Date;
import java.util.List;

public class CommitService {
    private final ICommitRepository commitRepository;

    public CommitService(ICommitRepository commitRepository) {
        this.commitRepository = commitRepository;
    }

    public void storeCommitInformation(int repoId, String message, Date commitDate) {
        CommitDTO commit = new CommitDTO(0,repoId,message,commitDate);
        commitRepository.createCommit(commit);
    }

    public List<CommitDTO> findCommits() {
        return commitRepository.findAllCommits();
    }
}
