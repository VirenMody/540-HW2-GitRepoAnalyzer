#Use Understand Python API to parse through a Java file in a Java Project

import understand

def fileCleanText(file):
    returnString = "";
    # Open the file lexer with macros expanded, inactive code removed, tabstop set to 8
    for lexeme in file.lexer(False,8,False,True):
        # Go through lexemes in the file and append
        # the text of non-comments to returnText
        print("token: " + lexeme.token() + " text: " + lexeme.text())
        # print(lexeme.text())
        if(lexeme.token() != "Comment"):
            returnString += lexeme.text()

    return returnString

# Open Database
db = understand.open("/home/guillermo/cs540/project.udb")

# Go through files in understand
for file in db.ents("File"):
    #Print directory name
    print(file.longname())

# Search for the first file named 'test' and print
# the file name and the cleaned text
file = db.lookup(".*test.*", "file")[0]

print(file.longname())
print(fileCleanText(file))

ents = db.ents()

# print entities sorted by name of entity
#for ent in sorted(ents, key=lambda ent: ent.longname()):
    #print(ent.longname(), "(", ent.parameters(), ")")

# print characteristics of unsorted entities
for ent in ents:
    print("Longname: " + ent.longname())
    print("Parameters: ", ent.parameters())
    print("Kind: ", ent.kind())
    print("Metric: ", ent.metrics())
    print("Parent: ", ent.parent())
    print("Type: ", ent.type())
    print("Name: ", ent.name())
    print("---")