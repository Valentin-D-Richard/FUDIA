import sys

USAGE = '''USAGE: python3 add_metadata.py [-o] [-i] [-n] FILE [-p PREFIX]
Adds the name of the file and a unique id as
first and second colum, and prints it in csv format

Options:
-i, --id        Adds a unique id
-n, --no-escape Does not escape or add double quotes
-o, --origin    Adds the origin file name
-p PREFIX       Prefix to unique id'''

ORIGIN = False
ID = False
NO_ESCAPE = False

# Handling paramters
if len(sys.argv) < 2 :
    print("ArgumentError: Need one file in argument", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    exit()

# Handling paramters
prefix = ""
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == "--help" or arg == "-h":
        print(USAGE)
        exit()
    elif arg == "-i" or arg == "--id":
        ID = True
    elif arg == "-o" or arg == "--origin":
        ORIGIN = True
    elif arg == "-n" or arg == "--no-escape":
        NO_ESCAPE = True
    elif arg == "-p" or arg == "--prefix":
        if i+1 >= len(sys.argv):
            print("No prefix given after flag -p", file=sys.stderr)
            print(USAGE, file=sys.stderr)
            exit()
        prefix = sys.argv[i+1] + "__"
        # extra __ added to fit Arborator id generator
        i += 1
    else:
        inputname = arg

    i += 1


# Opening file
input = open(inputname, "r")
origin = ".".join(inputname.split(".")[:-1])

# Adding two columns and writing in output
for k, line in enumerate(input):
    id = prefix + str(k+1)
    # escaping double quotes in line
    if NO_ESCAPE:
        new_line = line[:-1]
    else:
        new_line = "\""+ "\\\"".join(line[:-1].split("\"")) +"\""
    if ORIGIN:
        new_line = origin +","+ new_line
    if ID:
        new_line = id +","+ new_line
    print(new_line)

# Closing file
input.close()