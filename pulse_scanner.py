# Standard library to take input as command line argument
import sys

# Module to import some helper functions
from global_helpers import error, is_alpha, is_alnum, is_digit

# Module to import Token class
from token_class import

def string_val(source_code, i, table, line_num, start_char='"'):
    """
    Processes string values in the source code
    Params
    ======
    source_code (string) = The string containing simc source code
    i           (int)    = The current index in the source code
    table       (SymbolTable) = Symbol table constructed holding information about identifiers and constants
    line_num    (int)         = Line number
    Returns
    =======
    Token, int: The token generated for the string constant and the current position in source code,
                this is done only if there is no error in the string constant
    """

    string_constant = ""

    # Skip the first "/' so that the string atleast makes into the while loop
    i += 1

    # Loop until we get a non-digit character
    while source_code[i] != start_char:
        if source_code[i] == "\0":
            error("Unterminated string!", line_num)

        string_constant += source_code[i]
        i += 1

    # Skip the "/' character so that it does not loop back to this function incorrectly
    i += 1

    # Put appropriate quote
    string_constant = '"' + string_constant + '"'

    # Make entry in symbol table
    id = table.entry(string_constant, "string", "constant")

    # Return string token and current index in source code
    return Token("string", id, line_num), i
