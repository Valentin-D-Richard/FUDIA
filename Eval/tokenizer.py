import spacy
import sys

USAGE = '''USAGE: python3 tokenizer.py FILE
Tokenize each line of FILE and prints it'''

# Handling paramters
if len(sys.argv) != 2:
    print("ArgumentError: Need exactly one file in argument", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    exit()
elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print(USAGE)
    exit()
else:
    inputname = sys.argv[1]

# Create a Tokenizer with the default settings for French
# including punctuation rules and exceptions
tokenizer = spacy.load("fr_core_news_sm")

# Opening file
input = open(inputname, "r")

# Tokenizing and writing in output
for line in input:
    words = tokenizer(line.strip("\n"))
    print(" ".join([w.text for w in words]))

# Closing file
input.close()