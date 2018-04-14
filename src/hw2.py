from git import Repo, exc
from github3 import GitHub
from github3 import search_issues
import github3
import hw2_utils
import understand
import ntpath


#TODO Catch exception/error from invalid commits
# Creates understand databases from commits in passed pull_request
def create_und_db_from_pull_request(pull_request, path_to_local_clones):

    # Pull out information of first pull request
    (owner, repo_name, issue_num, pr_obj) = pull_request

    # Clone repository locally to selected path
    # Return full path of directory as a String
    commit_dir = clone_repo(owner, repo_name, path_to_local_clones, issue_num + 'current')
    parent_dir = clone_repo(owner, repo_name, path_to_local_clones, issue_num + 'parent')

    # Get the last commit in the list of commits (it is the most recent)
    (pr_commit_hash, pr_parent_hash) = select_last_commit(pr_obj)

    # Checkout pull-request's parent commit and create Understand DB on it
    error_code = hw2_utils.execute_command(['git', 'checkout', pr_parent_hash], parent_dir)
    if error_code != 0:
        raise Exception
    hw2_utils.create_und_db('pr_parent_commit.udb', parent_dir)

    # Checkout pull-request's commit and create Understand DB on it
    error_code = hw2_utils.execute_command(['git', 'checkout', pr_commit_hash], commit_dir)
    if error_code != 0:
        raise Exception
    hw2_utils.create_und_db('pr_current_commit.udb', commit_dir)

    return parent_dir, commit_dir


# TODO Return all commits
def select_last_commit(pr_obj):
    # Get the last commit in the list of commits (it is the most recent)
    commits = [commit.refresh() for commit in pr_obj.commits(-1, None)]
    pr_commits = commits[-1]
    pr_commit_hash = commits[-1].sha
    pr_parent_hash = commits[-1].parents[0]['sha']

    return (pr_commit_hash, pr_parent_hash)


# Return: local directory of the cloned repository
def clone_repo(owner, name, directory, commit_type):
    # TODO Update repository owner and name based on search results
    git_url = 'https://github.com/' + owner + '/' + name + '.git'
    repo_dir = directory + owner + name + commit_type

    try:
        # Clone the repository
        print('Cloning ' + owner + '/' + name + ' to repo directory: ' + repo_dir)
        cloned_repo = Repo.clone_from(git_url, repo_dir)
        assert cloned_repo.__class__ is Repo  # clone an existing repository

        return repo_dir
    # TODO Replace with logging
    except exc.GitError as err:
        print('***** ERROR CODE: 128 ******\n', err)
        print('*************************************************************************************************************')
        print('Cloned repositories still exist from the last run.\nPlease delete Cloned Repository directory.\nThen run again.')
        print('*************************************************************************************************************\n\n')
        exit(128)


# TODO Remove function if unused
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
def search_by_issues(git_hub, my_query, num):
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
        # TODO Remove if not necessary
        # else:
        #     continue

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


# returns tuple: (parent_dict, current_dict, key list of matches, key list of no matches,
#                   key list of items not in parent, key list of items not in current)
def understand_dict_parsing(und_db_path1, und_db_path2):
    parent_db = understand.open(und_db_path1)
    current_db = understand.open(und_db_path2)

    # Retrieve a list of all entities
    # - '~unresolved' entities are declared in Understand, but not defined
    # - '~volatile' only add non-volatile entities

    parent_db_dict = {}
    current_db_dict = {}

    for entity in parent_db.ents('~unresolved ~volatile'):
        key = str(entity.parent()) + '--' + str(entity.kind()) + '--' + entity.name()
        parent_db_dict[key] = entity

    for entity in current_db.ents('~unresolved ~volatile'):
        key = str(entity.parent()) + '--' + str(entity.kind()) + '--' + entity.name()
        current_db_dict[key] = entity

    print("Parent Keys")
    for key in sorted(parent_db_dict):
        print(key + ": " + str(parent_db_dict[key]))

    print("Current Keys")
    for key in sorted(current_db_dict):
        print(key + ": " + str(current_db_dict[key]))

    # parent to child changes
    match = 0
    no_match = 0
    not_in_parent_dict = 0
    not_in_commit_dict = 0

    match_ls = []
    no_match_ls = []
    not_in_parent_dict_ls = []
    not_in_commit_dict_ls = []
    for key in sorted(current_db_dict):
        if key not in parent_db_dict:
            not_in_parent_dict += 1
            print(key + " is in current dictionary but not in parent dictionary")
            not_in_parent_dict_ls.append(key)
            continue
        elif key in parent_db_dict and hw2_utils.is_entity_match(parent_db_dict[key], current_db_dict[key]):
            print(key + " is match.")
            match_ls.append(key)
            match += 1
        else:
            print(key + " is not match")
            no_match += 1
            no_match_ls.append(key)

    for key in sorted(parent_db_dict):
        if key not in current_db_dict:
            not_in_commit_dict += 1
            print(key + " is in parent dictionary but not in current dictionary")
            not_in_commit_dict_ls.append(key)

    return (parent_db_dict, current_db_dict, match_ls, no_match_ls, not_in_parent_dict_ls, not_in_commit_dict_ls)


def print_dict_parsing_results(match_ls, no_match_ls, not_in_parent_dict_ls, not_in_commit_dict_ls):
    print("total matches:" + str(len(match_ls)))
    print("list of matches")
    for i in match_ls:
        print(i)
    print("total mismatches:" + str(len(no_match_ls)))
    print("list of mismatches")
    for i in no_match_ls:
        print(i)
    print("total not in parent dictionary:" + str(len(not_in_parent_dict_ls)))
    print("list not in parent dictionary:")
    for i in not_in_parent_dict_ls:
        print(i)
    print("total not in commit dictionary:" + str(len(not_in_commit_dict_ls)))
    print("list not in commit dictionary:")
    for i in not_in_commit_dict_ls:
        print(i)



# TODO Make list of libraries/packages installed, specifications, etc.
# - github3.py
# - GitPython
# - Understand for Python https://scitools.com/support/python-api/
# - ntpath
# - Python Interpreter 3.6.3

# TODO add unit/integration testing
# TODO better commenting
# TODO exception handling
# TODO Give read access to professor
# TODO If possible avoid README pull request changes - invalid commit

# TODO Update the following to paths where commits are downloaded
GITHUB_USERNAME = 'virenmody'
GITHUB_ACCESS_TOKEN = 'a74c9704e00d767da4fe1d34aaf0ed8603d8ea11'

LOCAL_CLONED_REPO_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/ClonedRepos/'
DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/src/'
G_DB_PATH = '/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/src/'

G_ORIG_DB_PATH = '/home/guillermo/cs540/java_project.udb'
G_NEW_DB_PATH = '/home/guillermo/cs540/java_project2.udb'
G_LOCAL_CLONED_REPO_PATH = '/home/guillermo/cs540/cloned_repos/'

'''
#To use understand dictionary parsing 
understand_db1 = '/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/src/pr_parent_commit.udb'
understand_db2 = '/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/src/pr_current_commit.udb'
(parent_dict, current_dict, match, no_match, not_in_parent, not_in_commit) = understand_dict_parsing(understand_db1, understand_db2)
print_dict_parsing_results(match, no_match, not_in_parent, not_in_commit)
'''

# Create Pandas DataFrame to store changes
df_changes = hw2_utils.create_df()

# Authenticate GitHub object
git_hub = GitHub(GITHUB_USERNAME, GITHUB_ACCESS_TOKEN)

# TODO update the number of pull requests to retrieve
# Create Query and Search Pull Requests
query = "language:java is:pr label:bug is:closed"
pull_requests = 2

# Gets list of pull requests from repositories smaller than 50MB
# With pull requests that have been merged
pr_results = search_by_issues(git_hub, query, pull_requests)

for pr_data in pr_results:
    # Finds commits, checks out commits, creates understand database
    try:
        parent_repo_dir, current_repo_dir = create_und_db_from_pull_request(pr_data, LOCAL_CLONED_REPO_PATH)
    # TODO Replace print statements with logging
    except Exception as err:
        print('***** ERROR ******\n', err)
        print('*************************************************************************************************************')
        print('Possible: fatal: reference is not a tree: [commit]')
        print('Possible Invalid Commit: Skipping pull request, analyzing next')
        print('*************************************************************************************************************\n\n')
        continue

    # pr is the Pull Request Object
    pr = pr_data[3]

    # Open Database
    print(DB_PATH + 'pr_parent_commit.udb')
    print(DB_PATH + 'pr_current_commit.udb')
    parent_db = understand.open(DB_PATH + 'pr_parent_commit.udb')
    current_db = understand.open(DB_PATH + 'pr_current_commit.udb')

    # TODO Check if any files are added or removed
    # patch_files[index] Index: 0: added files, 1: modified files, 2: deleted files
    patch_files = hw2_utils.patch_files(pr.patch_url)
    modified_files = patch_files[1]

    # TODO Check if ntpath works on non-Windows systems
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    for PatchedFileObj in modified_files:
        print('Source Path: ', PatchedFileObj.source_file)
        print('Target Path: ', PatchedFileObj.target_file)
        print('Source Filename: ', ntpath.basename(PatchedFileObj.source_file))
        print('Target Filename: ', ntpath.basename(PatchedFileObj.target_file))
        parent_file = ntpath.basename(PatchedFileObj.source_file)
        current_file = ntpath.basename(PatchedFileObj.target_file)

        # TODO Catch this issue, if not remove it
        if parent_file != current_file:
            print('***************** WARNING: FILES DO NOT MATCH ***************************\n\n\n\n\n\n\n\n\n\n\n')
            exit(-99999999)

        # Retrieve file entity from database
        try:
            parent_file_ent = parent_db.lookup(parent_file, 'file')[0]
            current_file_ent = current_db.lookup(current_file, 'file')[0]
        except IndexError as err:
            print('***** ERROR ******\n', err)
            print('*************************************************************************************************************')
            print('File does not exist. Skipping pull request, analyzing next')
            print('*************************************************************************************************************\n\n')
            continue
        print('Parent File Entity: ', parent_file_ent)
        print('Current File Entity: ', current_file_ent)

        for HunkObj in PatchedFileObj:
            print('Added:   ', HunkObj.added)
            print('Removed: ', HunkObj.removed)

            parent_hunk_start = HunkObj.source_start
            parent_hunk_end = parent_hunk_start + HunkObj.source_length
            current_hunk_start = HunkObj.target_start
            current_hunk_end = current_hunk_start + HunkObj.target_length
            print('Source Start: ', parent_hunk_start, '   Length: ', HunkObj.source_length, '  End: ', parent_hunk_end)
            print('Target Start: ', current_hunk_start, '   Length: ', HunkObj.target_length, '  End: ', current_hunk_end)

            # TODO Maybe add an extra conditional confirming that total number of lines in each hunk are also equal
            if HunkObj.added == HunkObj.removed:
                parent_lexer = parent_file_ent.lexer()
                current_lexer = current_file_ent.lexer()
                # p_lxms = parent_lexer.lexemes(parent_hunk_start, parent_hunk_end)
                # c_lxms = current_lexer.lexemes(current_hunk_start, current_hunk_end)
                p_lxm = parent_lexer.first()
                c_lxm = current_lexer.first()

                num_changes_found = 0
                # TODO Ignore whitespace, newlines, punctuation?
                while p_lxm.next() is not None and c_lxm.next() is not None:

                    if num_changes_found == HunkObj.added:
                        break

                    # print(p_lxm.token().upper(), ':', p_lxm.text(), ' = ', c_lxm.text(), ':', c_lxm.token().upper())
                    # hw2_utils.understand_lexeme_info(p_lxm)
                    # if p_lxm.ent():
                    #     hw2_utils.understand_entity_info(p_lxm.ent())
                    try:
                        if p_lxm.text() != c_lxm.text():
                            print('Found difference: ', p_lxm.token().upper(), ':', p_lxm.text(), ' = ', c_lxm.text(), ':', c_lxm.token().upper())
                            if p_lxm.ref():
                                print('Parent line: ', p_lxm.ref().line())
                            if c_lxm.ref():
                                print('Current Line: ', c_lxm.ref().line())

                            change_category = '---'
                            before_value = p_lxm.text()
                            after_value = c_lxm.text()
                            filename = parent_file
                            scope = 'Unknown'
                            # TODO figure out occurrences
                            occurrence = 'TBD'

                            # Confirm that the change is of the same kindname (i.e. Variable, Data Type, etc.),
                            # otherwise, categorize as 'Uncategorized' and iterate to end of line

                            if p_lxm.ent() and c_lxm.ent():
                                if p_lxm.ent().kindname() != c_lxm.ent().kindname():
                                    print(p_lxm.text(), '--', p_lxm.ent().kind(), p_lxm.ent().kindname(), '::', c_lxm.ent().kind(), c_lxm.ent().kindname(), '--', c_lxm.text())
                                    if "Class" in p_lxm.ent().kindname() and "Class" in c_lxm.ent().kindname():
                                        change_category = 'Class'
                                if p_lxm.ent().kindname() == c_lxm.ent().kindname():
                                    change_category = p_lxm.ent().kindname()

                                    # Get filename if retrievable
                                    if p_lxm.ref() and c_lxm.ref() and p_lxm.ref().kindname() == c_lxm.ref().kindname():
                                        scope = p_lxm.ref().scope().name()

                            else:
                                # change_category = 'Uncategorized: KindMismatch'
                                while p_lxm.next().token() != 'Newline':
                                    # print(p_lxm.token().upper(), ':', p_lxm.text(), ' = ', c_lxm.text(), ':', c_lxm.token().upper())
                                    p_lxm = p_lxm.next()

                                while c_lxm.next().token() != 'Newline':
                                    # print(p_lxm.token().upper(), ':', p_lxm.text(), ' = ', c_lxm.text(), ':', c_lxm.token().upper())
                                    c_lxm = c_lxm.next()

                                # print(p_lxm.token().upper(), ':', p_lxm.text(), ' = ', c_lxm.text(), ':', c_lxm.token().upper())
                                # print('NEXT', p_lxm.next().token().upper(), ':', p_lxm.next().text(), ' = ', c_lxm.next().text(), ':', c_lxm.next().token().upper())

                                # Iterate to next lexeme
                                # p_lxm = p_lxm.next()
                                # c_lxm = c_lxm.next()
                                break

                            data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title]]
                            df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
                            num_changes_found += 1

                    except Exception as err:
                        print('Exception: ', err)
                        print(err.with_traceback())

                        # TODO Check to see if the mismatch lexemes' references are the same in the dependency graph
                        # TODO Check lexemes for the rest of that line before storing change

                    # Iterate to next lexeme
                    p_lxm = p_lxm.next()
                    c_lxm = c_lxm.next()

                print(df_changes)

            elif HunkObj.added == 0 or HunkObj.removed == 0:

                change_category = ''
                if HunkObj.added == 0:
                    change_category = 'Only Deletions'
                if HunkObj.removed == 0:
                    change_category = 'Only Insertions'
                before_value = 'N/A'
                after_value = 'N/A'
                filename = parent_file
                scope = 'Unknown'
                # TODO figure out occurrences
                occurrence = 'TBD'

                data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title]]
                df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
                print(df_changes)

            else:
                change_category = 'Uncategorized'
                before_value = 'N/A'
                after_value = 'N/A'
                filename = parent_file
                scope = 'Unknown'
                # TODO figure out occurrences
                occurrence = 'TBD'

                data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title]]
                df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
                print(df_changes)

    parent_db.close()
    current_db.close()

'''
Things to Consider
- IF STATEMENTS??
- Push lines of code in db with change for easy comparison
- Concatenate a whole line and look for token newline
- Use string contains to see whether a lexeme is in the string
- Consider a string diff tool to see how different they are

- Jump straight - to line numbers that indicate change
- Identify categories from the start using token or kind
- See which lexemes have kinds and references and handle exceptions

- Compare lines added to removed, some to 0 is deletion or addition
'''

