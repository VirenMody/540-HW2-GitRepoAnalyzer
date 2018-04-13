# from src import hw2_utils

from git import Repo
from github3 import GitHub
from github3 import search_issues
import github3
#import git
#import github3
import hw2_utils
import understand


def create_und_db_from_pull_request(result, path_to_local_clones):

    # Pull out information of first pull request
    (owner, repo_name, issue_num, pr_obj) = result

    # Clone repository locally to selected path
    # Return full path of directory as a String
    repo_dir = clone_repo(owner, repo_name, path_to_local_clones)

    # Get the last commit in the list of commits (it is the most recent)
    (pr_commit_hash, pr_parent_hash) = select_last_commit(pr_obj)

    # Checkout pull-request's parent commit and create Understand DB on it
    hw2_utils.execute_command(['git', 'checkout', pr_parent_hash], repo_dir)
    hw2_utils.create_und_db('pr_parent_commit.udb', repo_dir)

    # Checkout pull-request's commit and create Understand DB on it
    hw2_utils.execute_command(['git', 'checkout', pr_commit_hash], repo_dir)
    hw2_utils.create_und_db('pr_current_commit.udb', repo_dir)

    return True


def select_last_commit(pr_obj):
    # Get the last commit in the list of commits (it is the most recent)
    commits = [commit.refresh() for commit in pr_obj.commits(-1, None)]
    pr_commit_hash = commits[-1].sha
    pr_parent_hash = commits[-1].parents[0]['sha']

    return (pr_commit_hash, pr_parent_hash)


# Return: local directory of the cloned repository
def clone_repo(owner, name, directory):
    # TODO Update repository owner and name based on search results
    git_url = 'https://github.com/' + owner + '/' + name + '.git'
    repo_dir = directory + owner + name

    # Clone the repository
    print('Cloning ' + owner + '/' + name + ' to repo directory: ' + repo_dir)

    cloned_repo = Repo.clone_from(git_url, repo_dir)
    assert cloned_repo.__class__ is Repo  # clone an existing repository

    return repo_dir


# param: test_repo [Repository object],
def retrieve_one_closed_pull_request(test_repo):
    # Retrieve all 'CLOSED' pull requests
    pull_requests = [pr.refresh() for pr in test_repo.pull_requests('closed', None, None, 'created', 'desc', -1, None)]

    # TODO pull correct hash for pull request commit and parent commit
    # Retrieve the commits of all pull requests that have been merged and contain only 1 commit
    commits = []
    pr_commit_hash = ''
    pr_parent_hash = ''
    for pr in pull_requests:
        if pr.merged:
            commits = [commit.refresh() for commit in pr.commits(-1, None)]
            pr_commit_hash = commits[0].sha
            pr_parent_hash = commits[0].parents[0]['sha']

            print("pull request commit hash: " + pr_commit_hash)
            print("parent request commit hash: " + pr_parent_hash)
            # Checkout pull-request's parent commit and create Understand DB on it
            # hw2_utils.execute_command(['git', 'checkout', pr_parent_hash], repo_dir)
            # hw2_utils.create_und_db('pr_parent_commit.udb', repo_dir)

            # Checkout pull-request's commit and create Understand DB on it
            # hw2_utils.execute_command(['git', 'checkout', pr_commit_hash], repo_dir)
            # hw2_utils.create_und_db('pr_current_commit.udb', repo_dir)
            return pr

    return None


# Returns the pull request results of a search
# param: query
# param: number - the number of results to return
# return type: list, of 3 member tuples: [(user, repo name, issue #, pull request object)]
def search_by_issues(git_hub, my_query,num):
    # TODO Search for Github Java Repositories using issues/pull requests
    issue_search_result = git_hub.search_issues(query=my_query, number=num)
    results = []
    for item in issue_search_result:
        repo = item._json_data['repository_url']
        repo_arr = repo.split("/")
        username = repo_arr[4]
        repo_name = repo_arr[5]
        issue_number = str(item.issue.number)
        pull_request_url = item.issue.html_url
        repo_obj = git_hub.repository(username, repo_name)
        pr_obj = git_hub.pull_request(username, repo_name, issue_number)

        if (repo_obj.size < 50000) and (pr_obj.merged is True):
            results.append((username, repo_name, issue_number, pr_obj))
        else:
            continue

    return results


def search_by_repositories():
    # TODO Search for Github Java repositories
    # Query based off of size (less than 50 MB) and language (java)
    search_query = "language:java size:<50000"
    repo_search_result = git_hub.search_repositories(query=search_query, number=10)
    repos = []
    for i in repo_search_result:
        repos.append(i)

    print("repo search result")
    for repo in repos:
        print("Repo full name: " + repo.repository.full_name)

    return repos


def understand_simultaneous_entity_iteration():
    # Open Database
    print(DB_PATH + 'pr_parent_commit.udb')
    print(DB_PATH + 'pr_current_commit.udb')
    parent_db = understand.open(DB_PATH + 'pr_parent_commit.udb')
    current_db = understand.open(DB_PATH + 'pr_current_commit.udb')

    # Retrieve a list of all entities
    # - '~unresolved' entities are declared in Understand, but not defined
    # - '~volatile' TODO What is volatile
    # TODO limit which entities are retrieved based on patch files
    # TODO find list of kind search parameters
    parent_ents = parent_db.ents('~unresolved ~volatile')
    current_ents = current_db.ents('~unresolved ~volatile')

    # Iterate through entity lists to find and categorize differences
    diff_list = []

    for o_ent, n_ent in zip(parent_ents, current_ents):
        # Using understand_entity_info():
        # hw2_utils.understand_entity_info(o_ent)
        # hw2_utils.understand_entity_info(n_ent)

        print('Entities: {}:{}'.format(o_ent, n_ent), (o_ent == n_ent))
        # print('Name: {}:{}'.format(o_ent.name(), n_ent.name()), o_ent.name() == n_ent.name())
        # print('Parent: {}:{}'.format(o_ent.parent(), n_ent.parent()), o_ent.parent() == n_ent.parent())
        # print('Type: {}:{}'.format(o_ent.type(), n_ent.type()), o_ent.type() == n_ent.type())
        # print('Kind: {}:{}'.format(o_ent.kind(), n_ent.kind()), o_ent.kind() == n_ent.kind())
        # print('Value: {}:{}'.format(o_ent.value(), n_ent.value()), o_ent.value() == n_ent.value(), '\n')
        # print(o_ent.ref().file())

        if o_ent.name() != n_ent.name():
            print('Found a diff')
            diff_list.append(['name', o_ent.ref().file().name(), o_ent.name(), n_ent.name()])
        if o_ent.type() != n_ent.type():
            print('Found a diff')
            diff_list.append(['type', o_ent.ref().file().name(), o_ent.type().name, n_ent.type().name()])
        if o_ent.value() != n_ent.value():
            print('Found a diff')
            diff_list.append(['value', o_ent.ref().file().name(), o_ent.value(), n_ent.value()])

    print(diff_list)


def understand_dict_parsing():
    parent_db = understand.open('/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/und_db/squaresquash_before.udb')
    current_db = understand.open('/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/und_db/squaresquash_after.udb')

    # Retrieve a list of all entities
    # - '~unresolved' entities are declared in Understand, but not defined
    # - '~volatile' TODO What is volatile
    # TODO limit which entities are retrieved based on patch files
    # TODO find list of kind search parameters

    '''
    print("Parent Database------------------------------------")
    hw2_utils.print_entities(parent_db)
    print("Current Database------------------------------------")
    hw2_utils.print_entities(current_db)
    '''

    #with open('file.txt', 'w') as f:
    #print(hw2_utils.print_entities(current_db), file=f)

    parent_db_dict = {}
    current_db_dict = {}

    for entity in parent_db.ents('~unresolved ~volatile'):
        key = entity.name() + '-' + str(entity.kind()) + '-' + str(entity.parent())
        parent_db_dict[key] = entity

    for entity in current_db.ents('~unresolved ~volatile'):
        key = entity.name() + '-' + str(entity.kind()) + '-' + str(entity.parent())
        current_db_dict[key] = entity

    #print("Parent Database------------------------------------")
    #print(parent_db_dict)
    #print("Current Database------------------------------------")
    #print(current_db_dict)

    print("Parent Keys")
    for key in sorted(parent_db_dict):
        print(key + ": " + str(parent_db_dict[key]))

    print("Current Keys")
    for key in sorted(current_db_dict):
        print(key + ": " + str(current_db_dict[key]))

    parent_dict_checklist = parent_db_dict.copy()
    current_dict_checklist = current_db_dict.copy()

    # parent to child changes
    matches = 0
    no_matches = 0
    not_in_new_db = 0
    for key in sorted(parent_db_dict):
        if key not in current_db_dict:
            not_in_new_db+=1
            print(key + " is not in current dictionary")
            continue
        if key in current_db_dict and hw2_utils.is_entity_match(parent_db_dict[key], current_db_dict[key]):
            print (key + " is match.")
            matches+=1
            #print ("Parent Entity info")
            #hw2_utils.understand_entity_info(parent_db_dict[key])
            #print ("Current Entity info")
            #hw2_utils.understand_entity_info(current_db_dict[key])
        else:
            print (key + " is not match")
            no_matches+=1
            #print ("Parent Entity info")
            #hw2_utils.understand_entity_info(parent_db_dict[key])
            #print ("Current Entity info")
            #hw2_utils.understand_entity_info(current_db_dict[key])

    print("total matches:" + str(matches))
    print("total no matches:" + str(no_matches))
    print("total not in new dictionary:" + str(not_in_new_db))

    print("------Squash entry-------")
    hw2_utils.understand_entity_info(parent_db_dict['SquashEntry.message-Variable-squash.SquashEntry'])

    print("---Squash entry entities-------")
    hw2_utils.print_entities(parent_db_dict['SquashEntry.message-Variable-squash.SquashEntry'])


# TODO Make list of libraries/packages installed, specifications, etc.
# - github3.py
# - GitPython
# - Understand for Python https://scitools.com/support/python-api/

# - Python Interpreter 3.6.3
# TODO Update the following to paths where commits are downloaded
GITHUB_USERNAME = 'virenmody'
GITHUB_ACCESS_TOKEN = 'a74c9704e00d767da4fe1d34aaf0ed8603d8ea11'

LOCAL_CLONED_REPO_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/ClonedRepos/'

DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/src/'

G_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_ORIG_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_NEW_DB_PATH = '/home/guillermo/cs540/java_project2.udb'
G_LOCAL_CLONED_REPO_PATH = '/home/guillermo/cs540/cloned_repos/'

# Authenticate GitHub object
git_hub = GitHub(GITHUB_USERNAME, GITHUB_ACCESS_TOKEN)

# Create Query and Search Pull Requests
query = "language:java is:pr label:bug is:closed"
pull_requests = 10

# Gets list of pull requests from repositories smaller than 50MB
# With pull requests that have been merged
pr_results = search_by_issues(git_hub, query, pull_requests)

# Finds commits, checks out commits, creates understand database
create_und_db_from_pull_request(pr_results[0], G_LOCAL_CLONED_REPO_PATH)

# TODO Look into:
# - commits[0].files
# - pr.patch()
# - limiting number of commits per patch

