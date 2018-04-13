from src import hw2_utils

from git import Repo
from github3 import GitHub
# import hw2_utils
import understand
import ntpath


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

# TODO Update repository owner and name based on search results
repo_owner = 'SquareSquash'
repo_name = 'java'
git_url = 'https://github.com/' + repo_owner + '/' + repo_name + '.git'
parent_repo_dir = LOCAL_CLONED_REPO_PATH + repo_owner + repo_name + 'parent'
current_repo_dir = LOCAL_CLONED_REPO_PATH + repo_owner + repo_name + 'current'

# Clone the repository
# parent_cloned_repo = Repo.clone_from(git_url, parent_repo_dir)
# print('Cloned ' + repo_owner + '/' +repo_name + ' to repo directory: ' + parent_repo_dir)
# current_cloned_repo = Repo.clone_from(git_url, current_repo_dir)
# print('Cloned ' + repo_owner + '/' +repo_name + ' to repo directory: ' + current_repo_dir)

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
        hw2_utils.execute_command(['git', 'checkout', pr_parent_hash], parent_repo_dir)
        hw2_utils.create_und_db('pr_parent_commit.udb', parent_repo_dir)

        # Checkout pull-request's commit and create Understand DB on it
        hw2_utils.execute_command(['git', 'checkout', pr_commit_hash], current_repo_dir)
        hw2_utils.create_und_db('pr_current_commit.udb', current_repo_dir)

        # Open Database
        print(DB_PATH + 'pr_parent_commit.udb')
        print(DB_PATH + 'pr_current_commit.udb')
        parent_db = understand.open(DB_PATH + 'pr_parent_commit.udb')
        current_db = understand.open(DB_PATH + 'pr_current_commit.udb')

        # TODO Check if any files are added or removed
        # patch_files[index] Index: 0: added files, 1: modified files, 2: deleted files
        patch_files = hw2_utils.patch_files(pr.patch_url)
        modified_files = patch_files[1]

        # TODO Check if ntpath works on non-Windows systems (https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format)
        for PatchedFileObj in modified_files:
            print('Source Path: ', PatchedFileObj.source_file)
            print('Target Path: ', PatchedFileObj.target_file)
            print('Source Filename: ', ntpath.basename(PatchedFileObj.source_file))
            print('Target Filename: ', ntpath.basename(PatchedFileObj.target_file))
            parent_file = ntpath.basename(PatchedFileObj.source_file)
            current_file = ntpath.basename(PatchedFileObj.target_file)

            if(parent_file != current_file):
                print('***************** WARNING: FILES DO NOT MATCH ***************************\n\n\n\n\n\n\n\n\n\n\n')
                exit(-99999999)

            # Retrieve file entity from database
            parent_file_ent = parent_db.lookup(parent_file, 'file')[0]
            current_file_ent = current_db.lookup(current_file, 'file')[0]
            print('Parent File Entity: ', parent_file_ent)
            print('Current File Entity: ', current_file_ent)

            for HunkObj in PatchedFileObj:
                print('Added:   ', HunkObj.added)
                print('Removed: ', HunkObj.removed)

                parent_start = HunkObj.source_start
                parent_end = parent_start + HunkObj.source_length
                current_start = HunkObj.target_start
                current_end = current_start + HunkObj.target_length
                print('Source Start: ', parent_start, '   Length: ', HunkObj.source_length, '  End: ', parent_end)
                print('Target Start: ', current_start, '   Length: ', HunkObj.target_length, '  End: ', current_end)

                if HunkObj.added == HunkObj.removed:
                    parent_lexer = parent_file_ent.lexer()
                    current_lexer = current_file_ent.lexer()
                    par_lexemes = parent_lexer.lexeme(parent_start, parent_end)
                    cur_lexemes = current_lexer.lexeme(current_start, current_end)

                    while par_lexemes.next() is not None or cur_lexemes.next() is not None:
                        print(par_lexemes.text())
                        print(cur_lexemes.text())
                        if par_lexemes.text() != cur_lexemes.text():
                            print('Found a difference on line: ', par_lexemes.ref().line())
                            print('Found a difference on line: ', cur_lexemes.ref().line())
                            print(par_lexemes.text())
                            print(cur_lexemes.text())
                            # TODO Check to see if the mismatch lexemes' references are the same in the dependency graph

                        par_lexemes = par_lexemes.next()
                        cur_lexemes = cur_lexemes.next()


                    exit(-111)
