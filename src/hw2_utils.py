import urllib.request
from unidiff import PatchSet
import subprocess
import pandas as pd
from git import Repo, exc
import understand

    df_headers = ['ChangeCategory', 'BeforeValue', 'AfterValue', 'filename', 'scope', 'occurrence', 'prTitle', 'RepositoryName']


def create_und_db_from_pull_request(pr_data, path_to_local_clones):
    """
    Method creates 2 Understand databases: one for pull request commit, one for parent commit
    1) Clones repo for each commit
    2) Git checkout commit for each
    3) Creates Understand Database for each commit
    :param pr_data: tuple of owner, repo_name, issue number
    :param path_to_local_clones:
    :return:
    """

    # Pull out information of first pull request
    (owner, repo_name, issue_num, pr_obj) = pr_data

    # Clone repository locally to selected path
    # Return full path of directory as a String
    commit_dir = clone_repo(owner, repo_name, path_to_local_clones, issue_num + 'current')
    parent_dir = clone_repo(owner, repo_name, path_to_local_clones, issue_num + 'parent')

    # Get the last commit in the list of commits (it is the most recent)
    (pr_commit_hash, pr_parent_hash) = select_last_commit(pr_obj)

    # Todo: Windows: leave as is.
    # Todo: Ubuntu: Uncomment line  '# git_command = "git checkout " + pr_parent_hash'
    # Todo: Ubuntu: Uncomment line  '# error_code = execute_command(git_command, parent_dir)'
    # Todo: Ubuntu: Comment line    'error_code = execute_command(['git', 'checkout', pr_parent_hash], parent_dir)'
    # Checkout pull-request's parent commit and create Understand DB on it
    # git_command = "git checkout " + pr_parent_hash
    # error_code = execute_command(git_command, parent_dir)
    error_code = execute_command(['git', 'checkout', pr_parent_hash], parent_dir)
    if error_code != 0:
        raise Exception

    create_und_db('pr_parent_commit.udb', parent_dir)

    # Todo: Windows: leave as is.
    # Todo: Ubuntu: Uncomment line  '# git_command = "git checkout " + pr_commit_hash'
    # Todo: Ubuntu: Uncomment line  '# error_code = execute_command(git_command, commit_dir)'
    # Todo: Ubuntu: Comment line    'error_code = execute_command(['git', 'checkout', pr_commit_hash], commit_dir)'
    # Checkout pull-request's commit and create Understand DB on it
    # git_command = "git checkout " + pr_commit_hash
    # error_code = execute_command(git_command, commit_dir)
    error_code = execute_command(['git', 'checkout', pr_commit_hash], commit_dir)
    if error_code != 0:
        raise Exception

    create_und_db('pr_current_commit.udb', commit_dir)


# TODO Return all commits??
def select_last_commit(pr_obj):
    """
    Function retrieves the last of all commits within a pull request and its parent
    :param pr_obj: pull request object (contains list of related commits)
    :return: last pull request commit and parent commit
    """
    # Get the last commit in the list of commits (it is the most recent)
    commits = [commit.refresh() for commit in pr_obj.commits(-1, None)]
    pr_commits = commits[-1]
    pr_commit_hash = commits[-1].sha
    pr_parent_hash = commits[-1].parents[0]['sha']

    return (pr_commit_hash, pr_parent_hash)


def clone_repo(owner, name, directory, commit_type):
    """
    Function clones repository and returns local path to the repository
    :param owner: username
    :param name: repository name
    :param directory: where to clone repos
    :param commit_type: 'current' or 'parent' to distinguish pr commit and parent commit
    :return: local path to cloned repository
    """

    git_url = 'https://github.com/' + owner + '/' + name + '.git'
    # Path to locally cloned repo. commit_type distinguishes between pr commit and parent commit
    repo_dir = directory + owner + name + commit_type
    try:
        print('Cloning ' + owner + '/' + name + ' to repo directory: ' + repo_dir)
        cloned_repo = Repo.clone_from(git_url, repo_dir)
        assert cloned_repo.__class__ is Repo  # clone an existing repository
        return repo_dir

    # TODO Replace with logging
    except exc.GitError as err:
        print('***** CAUGHT ERROR: CODE: 128 ******\n', err)
        print('*************************************************************************************************************')
        print('Cloned repositories still exist from the last run.\nPlease delete Cloned Repository directory.\nThen run again.')
        print('*************************************************************************************************************\n\n')
        exit(128)


def search_by_issues(git_hub, my_query, num):
    """
    :param git_hub: authenticated GitHub object
    :param my_query: search query (i.e. java, closed, etc.)
    :param num: number of results to retrieve
    :return: results: tuple with username, repo name, issue number, and the pull request object
    """

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

        if (repo_obj.size < 30000) and (pr_obj.merged is True):
            results.append((username, repo_name, issue_number, pr_obj))

    return results


# TODO Comments for function
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
        elif key in parent_db_dict and is_entity_match(parent_db_dict[key], current_db_dict[key]):
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


# TODO Comments for function
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

# Understand Helper Functions
def understand_lexeme_info(lexeme):
    print("----------LEXEME INFO START-----------")
    print("Lexeme Text: ", lexeme.text())
    print("Token: ", lexeme.token())
    print("Entity: ", lexeme.ent())
    print("Column Begin:End: ", lexeme.column_begin(), ':', lexeme.column_end())
    print("Line Begin:End: ", lexeme.line_begin(), ':', lexeme.line_end())
    print("Reference: ", lexeme.ref())
    print("---------LEXEME INFO END------------")


def understand_entity_info(ent):
    print("----------ENTITY INFO START-----------")
    print("Entity Name: ", ent.name())
    # print("Annotations: ", str(ent.annotations()))
    # print("Comments: ", str(ent.comments()))
    print("Contents: ", ent.contents())
    # print("Lexer: ", ent.lexer())
    # print("Depends: ", ent.depends())
    # print("Depends By: ", ent.dependsby())
    # print("Entities: ", str(ent.ents("")))
    # print("Filerefs: ", str(ent.filerefs()))
    # print("ID: ", str(ent.id()))
    print("Kind: ", ent.kind())
    print("Kindname: ", ent.kindname())
    print("Language: " + ent.language())
    print("Library: " + ent.library())
    print("Longname: " + ent.longname())
    print("Metrics: ", str(ent.metrics()))
    print("Metric: ", ent.metric(ent.metrics()))
    # print("Name: ", ent.name())
    print("Parameters: ", ent.parameters())
    print("Parent: ", ent.parent())
    print("Ref: ", ent.ref())
    print("Refs: ", ent.refs())
    print("Type: ", ent.type())
    print("Uniquename: ", ent.uniquename())
    print("Value: ", ent.value())
    print("Info Browser: ", ent.ib())

    print("---------ENTITY INFO END------------")


def print_entities(db):
    current_ents = db.ents('~unresolved ~volatile')
    for ent in current_ents:
        understand_entity_info(ent)


def is_entity_match(ent1, ent2):
    if len(ent1.refs()) == len(ent2.refs()) and \
            len(ent1.ents("")) == len(ent2.ents("")):
        return True
    else:
        return False


def create_und_db(db_name, dir_to_analyze):
    """
    Function to create Understand database for repo for commit [hash]
    :param db_name: [repo database name].udb
    :param dir_to_analyze: path to repo to be analyzed
    :return: return code returned from execute_command function call
    """
    # Todo
    und_cmd = ['und', '-db', db_name, 'create', '-languages', 'java', 'add', dir_to_analyze, 'analyze']
    #g_und_cmd = 'und -db ' + db_name + ' create -languages java add ' + dir_to_analyze + ' analyze'
    return execute_command(und_cmd)


# TODO Remove console logging
def execute_command(command, dir=None):
    """
    Function executes given command on CLI (i.e. create udb files, checkout specific commits, etc.)
    :param command: to be executed on CLI
    :param dir: path to directory
    :return: return code from subprocess call
    """

    if dir is None:
        p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=False, cwd=dir, stdout=subprocess.PIPE)
    # Captures output, but errors are still displayed
    output = p.communicate()

    # Return Code: 0 (no error), 128 (possible: 'fatal: reference is not a tree: [commit]')
    return p.returncode


def get_files_from_patch(url):
    """
    Function parses patch file/url for affected files and returns a dictionary of files
    :param url: patch URL from pull request
    :return: files: dictionary of added, modified, and deleted files
    """
    diff = urllib.request.urlopen(url)
    # Assume encoding is utf-8
    patch = PatchSet(diff, encoding='utf-8')

    files = {'added_files': patch.added_files, 'modified_files': patch.modified_files, 'removed_files': patch.removed_files}

    return files


def create_df():
    """
    Function creates Python Pandas DataFrame used to store changes found in pull requests
    :return: data_frame: DataFrame
    """
    data_frame = pd.DataFrame(columns=df_headers)
    return data_frame


def add_row_to_df(df, new_row):
    """
    Function inserts each new change found when analyzing commits into DataFrame
    :param df: old Python Pandas DataFrame of change
    :param new_row: list of new change categorized
    :return: df: updated
    """
    new_df = pd.DataFrame(new_row, columns=df_headers)
    df = df.append(new_df, ignore_index=True)
    return df


# Check if script is running as main
if __name__ == "__main__":
    df = create_df()
