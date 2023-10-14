package com.company;

import DB.DatabaseConnection;
import GitVersionControl.GitVersionControl;

import java.sql.Connection;
import java.util.Date;

public class Main {

        public static void main(String[] args) {
            try {
                Connection dbConnection = DatabaseConnection.getConnection();
                String repoDirectory = "/D:/ТПРЗ/myRepo1";
                String gitExecutablePath = "C:\\Program Files\\Git\\cmd\\git.exe";
//        SVNVersionControl svn = new SVNVersionControl();
                GitVersionControl git = new GitVersionControl(dbConnection);
//        MercurialVersionControl mercurial = new MercurialVersionControl();
                git.initializeRepository(repoDirectory);
                git.commit("myRepo1", "file.txt.txt",0, "Git commit in branch dev 2",new Date());
                git.watchHistory("myRepo");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
