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

def numeric_val(source_code, i, table, line_num):
    """
    Processes numeric values in the source code
    Params
    ======
    source_code (string)      = The string containing pulse source code
    i           (int)         = The current index in the source code
    table       (SymbolTable) = Symbol table constructed holding information about identifiers and constants
    line_num    (int)         = Line number
    Returns
    =======
    Token, int: The token generated for the numeric constant and the current position in source code,
                this is done only if there is no error in the numeric constant
    """

    numeric_constant = ""

    # Loop until we get a non-digit character
    while is_digit(source_code[i]):
        numeric_constant += source_code[i]
        i += 1

    # If a numeric constant contains more than 1 decimal point (.) then that is invalid
    if numeric_constant.count(".") > 1:
        error(
            "Invalid numeric constant, cannot have more than one decimal point in a"
            " number!" , line_num
        )

    # Check the length after . to distinguish between float and double
    length = len(numeric_constant.split(".")[1]) if "." in numeric_constant else 0

    # Determine type of numeric value
    type = "int"
    if length != 0:
        if length <= 7:
            type = "float"
        elif length >= 7:
            type = "double"

    # Make entry in symbol table
    id = table.entry(numeric_constant, type, "constant")

    # Return number token and current index in source code
    return Token("number", id, line_num), i


