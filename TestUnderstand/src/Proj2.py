# Use Understand Python API to parse through a Java file in a Java Project

import understand
import itertools

def fileCleanText(file):
    returnString = ""
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
# db = understand.open("/home/guillermo/cs540/project.udb")
# db = understand.open("C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/project.udb")
dbOriginal = understand.open("C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb")
dbNew = understand.open("C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb")

# Go through files in understand
# for file in dbOriginal.ents("File"):
    # Print directory name
    # print(file.longname())

# Search for the first file named 'test' and print
# the file name and the cleaned text
# file = dbOriginal.lookup("Main.java", "file")[0]

# print(file.longname())
# print(fileCleanText(file))

# ents = dbOriginal.ents()

fileOriginal = dbOriginal.lookup("Main.java")[0]
fileNew = dbNew.lookup("Main.java")[0]
fileOriginal2 = dbOriginal.lookup("Main.java")[0]

print(fileOriginal==fileOriginal2)
print(fileOriginal==fileNew)

print(fileOriginal.ents("Java Method"))


#
# for lexeme in fileOriginal.lexer():
#   print (lexeme.text(),end="")
#   if lexeme.ent():
#     print ("@",end="")

# print entities sorted by name of entity
# for ent in sorted(ents, key=lambda ent: ent.longname()):
#     print(ent.longname(), "(", ent.parameters(), ")")

# print characteristics of unsorted entities
# for ent in ents:
#     print(ent.name())
#     print("Longname: " + ent.longname())
#     print("Parameters: ", ent.parameters())
#     print("Kind: ", ent.kind())
#     print("Metric: ", ent.metrics())
#     print("Parent: ", ent.parent())
#     print("Type: ", ent.type())
#     print("Name: ", ent.name())
#     print("---")
