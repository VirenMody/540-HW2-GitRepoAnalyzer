import understand

# TODO Retrieve Github pull requests and download commits

# TODO Update the following to paths where commits are downloaded
ORIG_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb'
NEW_DB_PATH = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb'

# TODO Create and execute a shell script to create udbs with downloaded commits
# Open Database
orig_db = understand.open(ORIG_DB_PATH)
new_db = understand.open(NEW_DB_PATH)

# Retrieve a list of all entities
# - '~unresolved' entities are declared in Understand, but not defined
# - '~volatile' TODO What is volatile
# TODO limit which entities are retrieved based on patch files
orig_ents = orig_db.ents('~unresolved ~volatile');
new_ents = new_db.ents('~unresolved ~volatile');

for o_ent, n_ent in zip(orig_ents, new_ents):
    print('Entities: {}:{}'.format(o_ent, n_ent), (o_ent == n_ent))
    print('Name: {}:{}'.format(o_ent.name(), n_ent.name()), o_ent.name() == n_ent.name())
    # print('Parent: {}:{}'.format(o_ent.parent(), n_ent.parent()), o_ent.parent() == n_ent.parent())
    # print('Type: {}:{}'.format(o_ent.type(), n_ent.type()), o_ent.type() == n_ent.type())
    # print('Kind: {}:{}'.format(o_ent.kind(), n_ent.kind()), o_ent.kind() == n_ent.kind())
    # print('Value: {}:{}'.format(o_ent.value(), n_ent.value()), o_ent.value() == n_ent.value(), '\n')

    # if o_ent == n_ent:
    #     if o_ent
