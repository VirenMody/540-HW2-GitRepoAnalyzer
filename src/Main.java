import org.eclipse.egit.github.core.*;
import org.eclipse.egit.github.core.service.*;
import org.eclipse.jgit.api.PushCommand;
import org.eclipse.jgit.api.RemoteAddCommand;
import org.eclipse.jgit.lib.StoredConfig;
import org.eclipse.jgit.transport.URIish;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.*;
import java.io.*;

import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.Transformer;



public class Main {


    public static void main(String[] args) {
        
        // TODO: Update the LOCAL_PATH variable to the directory where you want remote GitHub repositories to be downloaded
        // NOTE: GitHub Repositories are downloaded locally before they are uploaded to your local GitLab server.
        String LOCAL_PATH = "/home/virenmody/ClonedRepos/";


        //Initialize GitHub API repository Object to download repository from GitHub
        RepositoryService service = new RepositoryService();
        service.getClient();

        //Get list of repository results from GitHub API based on query
        String query = "maven junit language:java";
        List<SearchRepository> searchRepositoryList = null;

        try {
            searchRepositoryList = service.searchRepositories(query);
        }
        catch (IOException e){
            System.err.println("Caught IOException: " + e.getMessage());
        }

        //Create a Jenkins build for each repository in results list
        for (SearchRepository searchRepo: searchRepositoryList) {

            //Get current repository name and owner
            String projectName = searchRepo.getName();
            String username = searchRepo.getOwner();

            String repoURL = "https://github.com/" + username + "/" + projectName + ".git";
            String localDirectory = LOCAL_PATH + projectName;

            // Clone the Github repository to a local folder
            //      (RESOURCE: http://www.vogella.com/tutorials/JGit/article.html)
            Git clonedRepo = null;
            try {
                System.out.println("Cloning GitHub repo " + projectName + " to local directory: " + localDirectory);
                clonedRepo = Git.cloneRepository()
                        .setURI(repoURL)
                        .setDirectory(new File(localDirectory))
                        .call();
            } catch (GitAPIException e) {
                System.err.println("Caught GitAPIException: " + e.getMessage());
            }


        }

    }
}
