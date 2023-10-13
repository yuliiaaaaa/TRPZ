package GitVersionControl;

import java.util.Date;

public class MercurialVersionControl implements IVersionControlSystem {
    @Override
    public void commit(String repoName,String fileName, int repoId, String message, Date commitDate) {
        // Implement Git commit logic
    }

    @Override
    public void watchHistory(String repoName) {
        // Implement Git history display logic
    }
    @Override
    public void initializeRepository(String repoDirectory) {
    }
}
