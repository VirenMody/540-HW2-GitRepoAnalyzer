from src import hw2_utils

from git import Repo
from github3 import GitHub
import understand

# TODO Make list of libraries/packages installed, specifications, etc.
# - github3.py
# - GitPython
# - Understand for Python https://scitools.com/support/python-api/

# - Python Interpreter 3.6.3

# TODO Update the following to paths where commits are downloaded
GITHUB_USERNAME = 'virenmody'
GITHUB_ACCESS_TOKEN = 'a74c9704e00d767da4fe1d34aaf0ed8603d8ea11'

LOCAL_CLONED_REPO_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/ClonedRepos/'
ORIG_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/original.udb'
NEW_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/new.udb'
G_ORIG_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_NEW_DB_PATH = '/home/guillermo/cs540/java_project2.udb'

# Authenticate GitHub object
git_hub = GitHub(GITHUB_USERNAME, GITHUB_ACCESS_TOKEN)


# TODO Search for Github Java repositories

# TODO Update repository owner and name based on search results
repo_owner = 'SquareSquash'
repo_name = 'java'
git_url = 'https://github.com/' + repo_owner + '/' + repo_name + '.git'
repo_dir = LOCAL_CLONED_REPO_PATH + repo_owner + repo_name

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

        # Checkout pull-request's parent commit and create Understand DB on it
        hw2_utils.execute_command(['git', 'checkout', pr_parent_hash], repo_dir)
        hw2_utils.create_und_db('pr_parent_commit.udb', repo_dir)

        # Checkout pull-request's commit and create Understand DB on it
        hw2_utils.execute_command(['git', 'checkout', pr_commit_hash], repo_dir)
        hw2_utils.create_und_db('pr_commit.udb', repo_dir)

# TODO Look into:
# - commits[0].files
# - pr.patch()
# - limiting number of commits per patch

# Open Database
orig_db = understand.open(G_ORIG_DB_PATH)
new_db = understand.open(G_NEW_DB_PATH)

# Retrieve a list of all entities
# - '~unresolved' entities are declared in Understand, but not defined
# - '~volatile' TODO What is volatile
# TODO limit which entities are retrieved based on patch files
# TODO find list of kind search parameters
orig_ents = orig_db.ents('~unresolved ~volatile')
new_ents = new_db.ents('~unresolved ~volatile')


# Iterate through entity lists to find and categorize differences
diff_list = []

for o_ent, n_ent in zip(orig_ents, new_ents):
    # Using understand_entity_info():
    hw2_utils.understand_entity_info(o_ent)
    hw2_utils.understand_entity_info(n_ent)

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
