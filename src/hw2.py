import understand
import itertools

# TODO Retrieve Github pull requests and download commits

# TODO Update the following paths
ORIG_DB_PATH = "C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb"
NEW_DB_PATH = "C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb"

# Open Database
orig_db = understand.open(ORIG_DB_PATH)
new_db = understand.open(NEW_DB_PATH)

# Retrieve a list of all entities
orig_ents = orig_db.ents();
new_ents = new_db.ents();

for o_ent, n_ent in zip(orig_ents, new_ents):
    print('{} : {}'.format(o_ent, n_ent))