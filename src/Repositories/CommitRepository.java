package Repositories;

import Entities.CommitDTO;
import Repositories.ICommitRepository;

import java.sql.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class CommitRepository implements ICommitRepository {
    private Connection connection;

    public CommitRepository(Connection connection) {
        this.connection = connection;
    }


    public CommitDTO findByIdCommit(int id) {
        try {
            String sql = "SELECT * FROM commits WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, id);
            ResultSet resultSet = pstmt.executeQuery();

            if (resultSet.next()) {
                int commitId = resultSet.getInt("id");
                int repoId = resultSet.getInt("repo_id");
                String message = resultSet.getString("message");
                Date commitDate =resultSet.getDate("commit_date");

                return new CommitDTO(commitId, repoId, message,commitDate);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    public List<CommitDTO> findByRepoId(int repoId) {
        List<CommitDTO> commits = new ArrayList<>();

        try {
            String sql = "SELECT * FROM commits WHERE repo_id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, repoId);
            ResultSet resultSet = pstmt.executeQuery();

            while (resultSet.next()) {
                int commitId = resultSet.getInt("id");
                String message = resultSet.getString("message");
                Date commitDate =resultSet.getDate("commit_date");

                commits.add(new CommitDTO(commitId, repoId, message,commitDate));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return commits;
    }

    @Override
    public void createCommit(CommitDTO commit) {
        try {
            String sql = "INSERT INTO commits (repo_id, message,commit_date) VALUES (?, ?, ?)";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, commit.getRepoId());
            pstmt.setString(2, commit.getMessage());
            pstmt.setTimestamp(3, new Timestamp(commit.getCommitDate().getTime()));
            pstmt.executeUpdate();
            ResultSet generatedKeys = pstmt.getGeneratedKeys();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void updateCommit(CommitDTO commit) {
        try {
            String sql = "UPDATE commits SET message = ? WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setString(1, commit.getMessage());
            pstmt.setInt(2, commit.getId());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void deleteCommit(int id) {
        try {
            String sql = "DELETE FROM commits WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<CommitDTO> findAllCommits() {
        List<CommitDTO> commits = new ArrayList<>();

        try {
            String sql = "SELECT * FROM commits";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            ResultSet resultSet = pstmt.executeQuery();

            while (resultSet.next()) {
                int commitId = resultSet.getInt("id");
                int repoId = resultSet.getInt("repo_id");
                String message = resultSet.getString("message");
                Date commitDate = resultSet.getTimestamp("commit_date");

                commits.add(new CommitDTO(commitId, repoId, message, commitDate));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return commits;
    }
}
