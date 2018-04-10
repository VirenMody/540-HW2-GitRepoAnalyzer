from git import Repo
from github3 import GitHub
import understand
from src import hw2_utils
import subprocess

# TODO Make list of libraries/packages installed, specifications, etc.
# - github3.py
# - GitPython
# - Understand for Python https://scitools.com/support/python-api/

# - Python Interpreter 3.6.3

# TODO Update the following to paths where commits are downloaded
GITHUB_USERNAME = 'virenmody'
GITHUB_ACCESS_TOKEN = 'a74c9704e00d767da4fe1d34aaf0ed8603d8ea11'

LOCAL_CLONED_REPO_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/ClonedRepos/'
ORIG_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb'
NEW_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb'
G_ORIG_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_NEW_DB_PATH = '/home/guillermo/cs540/java_project2.udb'

# Authenticate GitHub object
git_hub = GitHub(GITHUB_USERNAME, GITHUB_ACCESS_TOKEN)

# TODO Search for Github Java repositories

# TODO Update repository owner and name based on search results
repo_owner = 'SquareSquash'
repo_name = 'java'
git_url = 'https://github.com/' + repo_owner + '/' + repo_name + '.git'
repo_dir = LOCAL_CLONED_REPO_PATH + repo_owner + '/' + repo_name
print(repo_dir)

# Retrieve repository object
test_repo = git_hub.repository(repo_owner, repo_name)

# Retrieve all 'CLOSED' pull requests
pull_requests = [pr.refresh() for pr in test_repo.pull_requests('closed', None, None, 'created', 'desc', -1, None)]

# Retrieve the commits of all pull requests that have been merged and contain only 1 commit
commits = []
for pr in pull_requests:
    if pr.merged:
        # if pr.commits_count == 1:
        print('Commit Title: ', pr.title)
        # print(pr.patch())
        commits = [commit.refresh() for commit in pr.commits(-1, None)]
        print('Files: ', commits[0].files)
        print('SHA: ', commits[0].sha)
        print('Parents: ', commits[0].parents)


# Clone the repository
cloned_repo = Repo.clone_from(git_url, repo_dir)
assert cloned_repo.__class__ is Repo     # clone an existing repository

sha = '5ee62f9977659e03e39406adcc4f6859e4524a0e'

# TODO Checkout pull request commit and the parent commit
cmd = ['git', 'checkout', sha]
p = subprocess.Popen(cmd, shell=True, cwd=repo_dir, stdout=subprocess.PIPE)
# p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in p.stdout:
    print('LINE: ', line)
p.wait()
print('RETURN CODE: ', p.returncode)

# TODO Create and execute a shell script to create udbs with downloaded commits
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
