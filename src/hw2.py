from github3 import GitHub
import understand
import hw2_utils

# TODO Retrieve Github pull requests and download commits
git_hub = GitHub("virenmody", "a74c9704e00d767da4fe1d34aaf0ed8603d8ea11")
print(git_hub)
repo_owner = 'SquareSquash'
repo_name = 'java'
test_repo = git_hub.repository(repo_owner, repo_name)
print(test_repo)
# pull_requests = test_repo.pull_requests('closed', None, None, 'created', 'desc', -1, None)
pull_requests = [pr.refresh() for pr in test_repo.pull_requests('closed', None, None, 'created', 'desc', -1, None)]
print(pull_requests)
for pr in pull_requests:
    # print(pr.title)
    if pr.merged:
        if pr.commits_count == 1:
            print(pr.title)
            print(pr.state)
            print(pr.merged)
            print(pr.patch())

# TODO Update the following to paths where commits are downloaded
ORIG_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb'
NEW_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb'
G_ORIG_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_NEW_DB_PATH = '/home/guillermo/cs540/java_project2.udb'

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
