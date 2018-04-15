from github3 import GitHub
import hw2_utils
import understand
import ntpath

# TODO Algorithm
# - Categorize changes in patch_files: file additions/deletions
# - Within 'Only Insertions' and 'Only Deletions' categorize what was added/removed
# TODO add unit/integration testing
# TODO add/improve comments
# TODO exception handling
# TODO Avoid invalid commits
# TODO Remove unnecessary print statements
# TODO Implement logging library
# TODO Optimize by not re-cloning already cloned repos

# TODO Update the following to paths where commits are downloaded
GITHUB_USERNAME = 'virenmody'
GITHUB_ACCESS_TOKEN = 'feec9be9b75ded7680e74e1be28b47c50564c2ac'

#Todo
LOCAL_CLONED_REPO_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/ClonedRepos/'
# LOCAL_CLONED_REPO_PATH = '/home/guillermo/cs540/cloned_repos/'
DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/src/'
# DB_PATH = '/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/src/'

# Create Pandas DataFrame to store changes found
df_changes = hw2_utils.create_df()

# Authenticate GitHub object
git_hub = GitHub(GITHUB_USERNAME, GITHUB_ACCESS_TOKEN)

# TODO update the number of pull requests to retrieve
# Create Query and Search Pull Requests
query = "language:java is:pr label:bug is:closed"

pull_requests = 10

# Gets list of merged pull requests from repositories smaller than 50MB
pr_results = hw2_utils.search_by_issues(git_hub, query, pull_requests)
print(pr_results)

for pr_data in pr_results:
    # Finds commits, checks out commits, creates understand database
    try:
        hw2_utils.create_und_db_from_pull_request(pr_data, LOCAL_CLONED_REPO_PATH)
    # TODO Replace print statements with logging
    except Exception as err:
        print('**************************************** ERROR CAUGHT ***********************************************************')
        print('Possible: fatal: reference is not a tree: [commit]')
        print('Possible Invalid Commit: Skipping pull request, analyzing next')
        print('*************************************************************************************************************\n\n')
        continue

    # pr_data[3] is the Pull Request Object
    pr = pr_data[3]

    # Open Database
    parent_db = understand.open(DB_PATH + 'pr_parent_commit.udb')
    current_db = understand.open(DB_PATH + 'pr_current_commit.udb')

    # From the patch file/url, retrieve a dictionary of files categorized as: added, modified, or removed files
    patch_files = hw2_utils.get_files_from_patch(pr.patch_url)

    # Check to see if any new files were added in the pull request, add change to df_changes
    for PatchedFileObj in patch_files['added_files']:
        added_file = ntpath.basename(PatchedFileObj.target_file)
        data_new_change = [['New File Added', 'N/A', added_file, added_file, 'N/A', 'TBD', pr.title]]
        df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)

    # Check to see if any files were removed in the pull request, add change to df_changes
    for PatchedFileObj in patch_files['removed_files']:
        removed_file = ntpath.basename(PatchedFileObj.source_file)
        data_new_change = [['File Removed', 'N/A', removed_file, removed_file, 'N/A', 'TBD', pr.title]]
        df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)

    # For each modified file, identify changes in modified files, add change to df_changes
    for PatchedFileObj in patch_files['modified_files']:
        parent_file = ntpath.basename(PatchedFileObj.source_file)
        current_file = ntpath.basename(PatchedFileObj.target_file)

        # Since added and removed files have been processed above, modified file mismatch means the file was renamed.
        if parent_file != current_file:
            data_new_change = [['File Renamed', parent_file, current_file, current_file, 'N/A', 'TBD', pr.title]]
            df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
            continue

        # Since we are identifying changes per file, retrieve file entity from database
        try:
            parent_file_ent = parent_db.lookup(parent_file, 'file')[0]
            current_file_ent = current_db.lookup(current_file, 'file')[0]
        except IndexError as err:
            print('***** INDEX ERROR CAUGHT ******\n', err)
            print('*************************************************************************************************************')
            print('File does not exist. Skipping pull request, analyzing next')
            print('*************************************************************************************************************\n\n')
            continue

        # Each modified file's changes are broken down into hunks, for each hunk find and store changes
        for HunkObj in PatchedFileObj:
            parent_hunk_start = HunkObj.source_start
            parent_hunk_end = parent_hunk_start + HunkObj.source_length
            current_hunk_start = HunkObj.target_start
            current_hunk_end = current_hunk_start + HunkObj.target_length

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
                # Loop through lexeme to identify mismatches and then categorize the change
                while p_lxm.next() is not None and c_lxm.next() is not None:

                    # After all changes are found for the given hunk, break loop and move on to next hunk
                    if num_changes_found == HunkObj.added:
                        break

                    try:
                        # When a difference is found, categorize change and add it to the dataframe
                        if p_lxm.text() != c_lxm.text():

                            # Initialize values for dataframe
                            change_category = 'Uncategorized'
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

                            # If the mismatch represent lexemes that are not entities, the change is not manageable, iterate to the end of the line and break to the next
                            else:
                                # change_category = 'Uncategorized: KindMismatch'
                                # Iterate parent lexeme to the end of the line of code
                                while p_lxm.next().token() != 'Newline':
                                    p_lxm = p_lxm.next()
                                # Iterate current lexeme to the end of the line of code
                                while c_lxm.next().token() != 'Newline':
                                    c_lxm = c_lxm.next()
                                break

                            data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title, pr_data[0] + "/" + pr_data[1]]]
                            df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
                            num_changes_found += 1

                    except Exception as err:
                        print('Exception: ', err)
                        # print(err.with_traceback())

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

                data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title, pr_data[0] + "/" + pr_data[1]]]
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

                data_new_change = [[change_category, before_value, after_value, filename, scope, occurrence, pr.title,pr_data[0] + "/" + pr_data[1]]]
                df_changes = hw2_utils.add_row_to_df(df_changes, data_new_change)
                print(df_changes)

    parent_db.close()
    current_db.close()

print(df_changes)
df_changes.to_csv('analysis.csv', sep=',', na_rep='', index=False)

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

