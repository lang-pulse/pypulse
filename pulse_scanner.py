# Standard library to take input as command line argument
import sys

# Import some helper functions
from global_helpers import error, is_alpha, is_alnum, is_digit

# Import Token class
from token_class import Token

# Import Scanner class
from scanner_class import Scanner

def is_keyword(value):
    """
    Checks if string is keyword or not
    Params
    ======
    value (string) = The string to be checked for keyword
    Returns
    =======
    bool: Whether the value passed is a keyword or not
    """
    return value in [
        "and",
        "or",
        "var",
        "print",
        "while",
        "input",
        "if",
        "else",
        "class",
        "fun",
        "for",
        "do",
        "not",
        "true",
        "false",
        "elif"
    ]

def keyword_identifier(source_code, i, table, line_num, scanner):
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

def string_val(source_code, i, table, line_num, scanner, start_char='"'):
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
    print(source_code[i:])

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

def numeric_val(source_code, i, table, line_num, scanner):
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

def checkUnindent(source_code, i, table, line_num, scanner):
    """
    processes indentation in the source code

    Params
    ======
    source_code (string) = The string containing simc source code
    i           (int)    = The current index in the source code
    table       (SymbolTable) = Symbol table constructed holding information about identifiers and constants
    line_num    (int)         = Line number

    Returns
    =======
    int: the current position in source code
    """
    #checks if the code is indented following ':'
    if (scanner.isIndent):
        localTabCount = 0
        while (source_code[i+1] == "\t"):
            localTabCount += 1
            i += 1
        if (source_code[i] == "\t"):
            i += 1
        if (localTabCount < scanner.indentLevel):
            scanner.isUnindent = True
            scanner.unindentLevel = scanner.indentLevel - localTabCount - 1
            if (localTabCount == 0):
                scanner.indentLevel = 0
            else:
                scanner.indentLevel -= 1

            if (scanner.unindentLevel > 0 and localTabCount != 0):
                if (scanner.unindentLevel -1 > 0):
                    scanner.indentLevel = scanner.unindentLevel - 1
                else:
                    scanner.indentLevel = localTabCount

        if (scanner.indentLevel == 0):
            scanner.isIndent = False
    else:
        i += 1

    return i


def scanner(source_code, table):
    """
    Generate tokens from source code
    Params
    ======
    filename    (string)      = The string containing simc source code filename
    table       (SymbolTable) = Symbol table constructed holding information about identifiers and constants
    Returns
    ========
    list: A list of tokens of the source code, if the code is lexically correct, otherwise
          presents user with an error
    """

    # Create scanner class' object
    scanner = Scanner()

    #Loop through the source code character by character
    i = 0
    while source_code[i] != "\0":
        # If a digit appears, call numeric_val function and add the numeric token to list,
        # if it was correct
        if is_digit(source_code[i]):
            token, i = numeric_val(source_code, i, table, scanner.line_num, scanner)
            scanner.tokens.append(token)

        # If quote appears the value is a string token
        elif source_code[i] == '"':
            token, i = string_val(source_code, i, table, scanner.line_num, scanner)
            scanner.tokens.append(token)

        elif source_code[i] == '\'':
            token, i = string_val(source_code, i, table, scanner.line_num, scanner, '\'')
            scanner.tokens.append(token)

        # If alphabet or number appears then it might be either a keyword or an identifier
        elif is_alnum(source_code[i]):
            token, i = keyword_identifier(source_code, i, table, scanner.line_num, scanner)
            scanner.tokens.append(token)

        elif (source_code[i] == ":"):
            scanner.isIndent = True
            scanner.indentLevel += 1
            if (source_code[i+1] == "\n"):
                scanner.line_num += 1
                i += 1
                i = checkUnindent(source_code, i, table, scanner.line_num, scanner)
            token = Token("begin_block", "", scanner.line_num)
            scanner.tokens.append(token)

        elif (source_code[i] == "\n"):
            scanner.line_num += 1
            i = checkUnindent(source_code, i, table, scanner.line_num, scanner)
            token = Token("newline", "", scanner.line_num)
            scanner.tokens.append(token)

        else:
            i += 1

    return scanner.tokens
