package GitVersionControl;

import java.util.Date;

public class SVNVersionControl implements IVersionControlSystem {
    @Override
    public void commit(String repoName,String fileName, int repoId, String message, Date commitDate) {
        // Implement SVN commit logic
    }

    @Override
    public void watchHistory(String repoName) {
        // Implement SVN history display logic
    }

    @Override
    public void initializeRepository(String repoDirectory) {
    }
}