frofrom global_helpers import error, is_alpha, is_alnum, is_digit
import sys
from token_class import Token

def keyword_identifier(source_code, i, table, line_num):
    """
    Process keywords and identifiers in source code
    Params
    ======
    source_code (string) = The string containing simc source code
    i           (int)    = The current index in the source code
    table       (SymbolTable) = Symbol table constructed holding information about identifiers and constants
    line_num    (int)         = Line number
    Returns
    =======
    Token, int: The token generated for the keyword or identifier and the current position in source code
    """ 
    #an empty string is assigned to value"
    value = ""

    # Loop until we get a non-digit character
    while is_alnum(source_code[i]):
        value += source_code[i]
        i += 1

    # Check if value is keyword or not
    if is_keyword(value):
        return Token(value, "", line_num), i

    # Check if identifier is in symbol table
    id = table.get_by_symbol(value)

    # If identifier is not in symbol table then give a placeholder datatype var
    if id == -1:
        id = table.entry(value, "var", "variable")

     
    # Returns the  id, token and current index in source code
    return Token("id", id, line_num), i

