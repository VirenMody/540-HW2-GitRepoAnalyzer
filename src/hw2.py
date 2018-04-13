# from src import hw2_utils

from git import Repo
from github3 import GitHub
from github3 import search_issues
import github3
#import git
#import github3
import hw2_utils
import understand


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


# TODO Search for Github Java repositories

q = "language:java is:pr label:bug is:closed"
issue_search_result = git_hub.search_issues(query=q, number=10)
issues = []
for i in issue_search_result:
    issues.append(i)

print("html urls for all issues")
for i in issues:
    print(i.issue.html_url)
    print(i._json_data['repository_url'])


print("issue search result")
print(issue_search_result)


# TODO Update repository owner and name based on search results
repo_owner = 'SquareSquash'
repo_name = 'java'
git_url = 'https://github.com/' + repo_owner + '/' + repo_name + '.git'
repo_dir = G_LOCAL_CLONED_REPO_PATH + repo_owner + repo_name

# Clone the repository
print('Cloning ' + repo_owner + '/' +repo_name + ' to repo directory: ' + repo_dir)


cloned_repo = Repo.clone_from(git_url, repo_dir)
assert cloned_repo.__class__ is Repo  # clone an existing repository

# Retrieve repository object
test_repo = git_hub.repository(repo_owner, repo_name)

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
        break

# TODO Look into:
# - commits[0].files
# - pr.patch()
# - limiting number of commits per patch

