package DB;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static final String url = "jdbc:postgresql://localhost:5432/repositories";
    private static final String user = "postgres";
    private static final String password = "postgres";
    private static Connection connection;

    public static Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            connection = DriverManager.getConnection(url, user, password);
        }
        if (connection != null) {
            System.out.println("Connected to the database successfully.");
        }
        return connection;
    }
}
