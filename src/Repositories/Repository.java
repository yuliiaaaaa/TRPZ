package Repositories;
import Entities.RepositoryDTO;
import Repositories.IRepository;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class Repository implements IRepository<RepositoryDTO> {
    private Connection connection;

    public Repository(Connection connection) {
        this.connection = connection;
    }

    @Override
    public RepositoryDTO findById(int id) {
        try {
            String sql = "SELECT * FROM repositories WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, id);
            ResultSet resultSet = pstmt.executeQuery();

            if (resultSet.next()) {
                int repoId = resultSet.getInt("id");
                String name = resultSet.getString("name");
                String type = resultSet.getString("type");

                return new RepositoryDTO(repoId, name, type);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    public List<RepositoryDTO> findAll() {
        List<RepositoryDTO> repositories = new ArrayList<>();

        try {
            String sql = "SELECT * FROM repositories";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            ResultSet resultSet = pstmt.executeQuery();

            while (resultSet.next()) {
                int repoId = resultSet.getInt("id");
                String name = resultSet.getString("name");
                String type = resultSet.getString("type");

                repositories.add(new RepositoryDTO(repoId, name, type));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return repositories;
    }

    @Override
    public void create(RepositoryDTO entity) {
        try {
            String sql = "INSERT INTO repositories (name, type) VALUES (?, ?)";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setString(1, entity.getName());
            pstmt.setString(2, entity.getType());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void update(RepositoryDTO entity) {
        try {
            String sql = "UPDATE repositories SET name = ?, type = ? WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setString(1, entity.getName());
            pstmt.setString(2, entity.getType());
            pstmt.setInt(3, entity.getId());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void delete(int id) {
        try {
            String sql = "DELETE FROM repositories WHERE id = ?";
            PreparedStatement pstmt = connection.prepareStatement(sql);
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}