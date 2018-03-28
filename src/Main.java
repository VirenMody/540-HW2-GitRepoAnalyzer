import org.eclipse.egit.github.core.SearchRepository;
import org.eclipse.egit.github.core.service.RepositoryService;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;

import java.io.File;
import java.io.IOException;
import java.util.List;



public class Main {


    public static void main(String[] args) {
        
        // TODO: Update the LOCAL_PATH variable to the directory where you want remote GitHub repositories to be downloaded
        // NOTE: GitHub Repositories are downloaded locally before they are uploaded to your local GitLab server.
        String LOCAL_PATH = "/Users/Viren/Google Drive/1. UIC/540 - Advanced Software Engineering Topics/ClonedRepos/";


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
