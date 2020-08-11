#The module for system-specific parameters and functions
import sys

# Import SymbolTable class
from symbol_table_class import SymbolTable

# Import scanner
from pulse_scanner import scanner

def readFile(path):
    """
    Reads a file and returns the contents as a string

    Params
    ======
    path (string) : PAth to file which is to be read

    Returns
    =======
    buffer (string) : Contents of the file
    """
    try:
        # open the file in read mode
        file = open(path, "r")
    except:
        # if file cannot be opened
        sys.stderr.write("Could not open %s" % (path))
        exit(74)

    #reading the file
    if file.mode == "r":
        buffer = file.read()
        #Add a EOF token to end of source code
        buffer += "\0"

    file.close()

    return buffer


# Read file path from command line
file_path = sys.argv[1]

# Get the source code form code file
source_code = readFile(file_path)

# Create symbol table
table = SymbolTable()

# Pass source code to lexical analyzer
tokens = scanner(source_code, table)

for token in tokens:
    print(token)

# TODO: Pass tokens into parser and compiler

# TODO: Pass bytecode into VM for execution
