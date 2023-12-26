package GitVersionControl;

import java.util.Date;

public interface IVersionControlSystem {
    void commit(String repoName,String fileName, int repoId, String message, Date commitDate);
    void watchHistory(String repoName);
    void initializeRepository(String repoDirectory);
}

