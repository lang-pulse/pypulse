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
    value (str)
        : The string to be checked for keyword
    Returns
    =======
    (bool)
        : Whether the value passed is a keyword or not
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
        "elif",
    ]


def keyword_identifier(source_code, i, table, scanner_obj):
    """
    Process keywords and identifiers in source code
    Params
    ======
    source_code (str)
        : The string containing pulse source code
    i           (int)
        : The current index in the source code
    table       (SymbolTable)
        : Symbol table constructed holding information about identifiers and constants
    scanner_obj (Scanner)
        : Instance of Scanner class
    Returns
    =======
    (Token)
        : The token generated for the keyword or identifier
    (int)
        : Current position in source code
    """

    value = ""

    # Loop until we get a non-digit character
    while is_alnum(source_code[i]):
        value += source_code[i]
        i += 1

    # Check if value is keyword or not
    if is_keyword(value):
        return Token(value, "", scanner_obj.line_num), i

    # Check if identifier is in symbol table
    id = table.get_by_symbol(value)

    # If identifier is not in symbol table then give a placeholder datatype var
    if id == -1:
        id = table.entry(value, "var", "variable")

    # Returns the  id, token and current index in source code
    return Token("id", id, scanner_obj.line_num), i


def string_val(source_code, i, table, scanner_obj, start_char='"'):
    """
    Processes string values in the source code
    Params
    ======
    source_code (str)
        : The string containing simc source code
    i           (int)
        : The current index in the source code
    table       (SymbolTable)
        : Symbol table constructed holding information about identifiers and constants
    scanner_obj (Scanner)
        : Instance of Scanner class
    start_char  (str) (Optional)
        : Character with which string starts
    Returns
    =======
    (Token)
        : The token generated for the string constant
    (int)
        : Current position in source code
    """

    string_constant = ""

    # Skip the first "/' so that the string atleast makes into the while loop
    i += 1

    # Loop until we get a non-digit character
    while source_code[i] != start_char:
        if source_code[i] == "\0":
            error("Unterminated string!", scanner_obj.line_num)

        string_constant += source_code[i]
        i += 1

    # Skip the "/' character so that it does not loop back to this function incorrectly
    i += 1

    # Put appropriate quote
    string_constant = '"' + string_constant + '"'

    # Make entry in symbol table
    id = table.entry(string_constant, "string", "constant")

    # Return string token and current index in source code
    return Token("string", id, scanner_obj.line_num), i


def numeric_val(source_code, i, table, scanner_obj):
    """
    Processes numeric values in the source code
    Params
    ======
    source_code (str)
        : The string containing simc source code
    i           (int)
        : The current index in the source code
    table       (SymbolTable)
        : Symbol table constructed holding information about identifiers and constants
    scanner_obj (Scanner)
        : Instance of Scanner class
    Returns
    =======
    (Token)
        : The token generated for the numeric constant
    (int)
        : Current position in source code
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
            " number!",
            scanner_obj.line_num,
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
    return Token("number", id, scanner_obj.line_num), i


def check_unindent(source_code, i, table, scanner_obj):
    """
    Processes indentation in the source code
    Params
    ======
    source_code (str)
        : The string containing pulse source code
    i           (int)
        : The current index in the source code
    table       (SymbolTable)
        : Symbol table constructed holding information about identifiers and constants
    scanner_obj (Scanner)
        : Instance of Scanner class
    Returns
    =======
    (int)
        : the current position in source code
    """

    # Checks if the code is indented following ':'
    if scanner_obj.isIndent:
        # Count spaces/tabs
        localTabCount = 0
        localSpaceCount = 0
        while source_code[i] == "\t":
            localTabCount += 1
            i += 1
        while source_code[i] == " ":
            localSpaceCount += 1
            i += 1

        # Convert spaces into tabs
        localTabCount = localSpaceCount // 2 if localTabCount == 0 else localTabCount

        # If the number of tabs before a line are less than the current level of indentation then setup unindentation
        if localTabCount < scanner_obj.indentLevel:
            scanner_obj.isUnindent = True
            scanner_obj.unindentLevel = scanner_obj.indentLevel - localTabCount

        # If scanner's indentation level is zero then set isIndent to false
        if scanner_obj.indentLevel == 0:
            scanner_obj.isIndent = False

    return i


def gen_unindent(scanner_obj):
    """
    Generates unindent token
    Params
    ======
    scanner_obj (Scanner)
        : Instance of Scanner class
    """

    if scanner_obj.unindentLevel > 0:
        print("Here-", scanner_obj.indentLevel)
        while scanner_obj.unindentLevel != 0:
            token = Token("unindent", "", scanner_obj.line_num)
            scanner_obj.tokens.append(token)

            scanner_obj.unindentLevel -= 1
            scanner_obj.indentLevel -= 1

        scanner_obj.isIndent = False


def scanner(source_code, table):
    """
    Generate tokens from source code
    Params
    ======
    source_code (str)
        : Pulse source code
    table       (SymbolTable)
        : Symbol table constructed holding information about identifiers and constants
    Returns
    ========
    tokens: A list of tokens of the source code
    """

    # Create scanner_obj class' object
    scanner_obj = Scanner()

    # Loop through the source code character by character
    i = 0

    # To store comments string
    comment_str = ""

    while source_code[i] != "\0":
        # If a digit appears, call numeric_val function and add the numeric token to list,
        # if it was correct
        if is_digit(source_code[i]):
            token, i = numeric_val(source_code, i, table, scanner_obj)
            scanner_obj.tokens.append(token)

        # If double quote appears the value is a string token
        elif source_code[i] == '"':
            token, i = string_val(source_code, i, table, scanner_obj)
            scanner_obj.tokens.append(token)

        # If single quote appears the value is a string token
        elif source_code[i] == "'":
            token, i = string_val(source_code, i, table, scanner_obj, "'")
            scanner_obj.tokens.append(token)

        # If alphabet or number appears then it might be either a keyword or an identifier
        elif is_alnum(source_code[i]):
            token, i = keyword_identifier(source_code, i, table, scanner_obj)
            scanner_obj.tokens.append(token)

        # If character is : then generate begin block token and start indentation
        elif source_code[i] == ":":
            token = Token("begin_block", "", scanner_obj.line_num)
            scanner_obj.tokens.append(token)
            scanner_obj.isIndent = True
            scanner_obj.indentLevel += 1
            i += 1

        # If character is \n then generate newline token and check for unindentation
        elif source_code[i] == "\n":
            scanner_obj.line_num += 1
            token = Token("newline", "", scanner_obj.line_num)
            scanner_obj.tokens.append(token)
            i = check_unindent(source_code, i + 1, table, scanner_obj)
            gen_unindent(scanner_obj)

        # If character is ( then generate left paren token
        elif source_code[i] == "(":
            scanner_obj.tokens.append(Token("left_paren", "", scanner_obj.line_num))
            i += 1

        # If character is ) then generate right paren token
        elif source_code[i] == ")":
            scanner_obj.tokens.append(Token("right_paren", "", scanner_obj.line_num))
            i += 1

        # Identifying Left brace token
        elif source_code[i] == "{":
            scanner_obj.tokens.append(Token("left_brace", "", scanner_obj.line_num))
            i += 1

        # Identifying right brace token
        elif source_code[i] == "}":
            scanner_obj.tokens.append(Token("right_brace", "", scanner_obj.line_num))
            i += 1

        # Identifying assignment or equal token
        elif source_code[i] == "=":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(Token("equal", "", scanner_obj.line_num))
                i += 2
            else:
                scanner_obj.tokens.append(Token("assignment", "", scanner_obj.line_num))
                i += 1

        # Identifying plus equal, increment or plus token
        elif source_code[i] == "+":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(Token("plus_equal", "", scanner_obj.line_num))
                i += 2
            elif source_code[i + 1] == "+":
                scanner_obj.tokens.append(Token("increment", "", scanner_obj.line_num))
                i += 2
            else:
                scanner_obj.tokens.append(Token("plus", "", scanner_obj.line_num))
                i += 1

        # Identifying minus equal, decrement or minus token
        elif source_code[i] == "-":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("minus_equal", "", scanner_obj.line_num)
                )
                i += 2
            elif source_code[i + 1] == "-":
                scanner_obj.tokens.append(Token("decrement", "", scanner_obj.line_num))
                i += 2
            else:
                scanner_obj.tokens.append(Token("minus", "", scanner_obj.line_num))
                i += 1

        # Identifying multiply equal or multiply token
        elif source_code[i] == "*":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("multiply_equal", "", scanner_obj.line_num)
                )
                i += 2
            else:
                scanner_obj.tokens.append(Token("multiply", "", scanner_obj.line_num))
                i += 1

        # Identifying single line comment token
        elif source_code[i] == "#":
            i += 1
            while source_code[i] != "\n":
                comment_str += str(source_code[i])
                i += 1
            scanner_obj.tokens.append(
                Token("single_line_comment", comment_str, scanner_obj.line_num)
            )
            comment_str = ""

        # Identifying multi line comment, divide_equal, integer_divide, divide token
        elif source_code[i] == "/":
            if source_code[i + 1] == "*":
                i += 2
                while source_code[i] != "*" and source_code[i + 1] != "/":
                    comment_str += str(source_code[i])
                    i += 1
                scanner_obj.tokens.append(
                    Token("multi_line_comment", comment_str, scanner_obj.line_num)
                )
                comment_str = ""
            elif source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("divide_equal", "", scanner_obj.line_num)
                )
                i += 2

            elif source_code[i + 1] == "/":
                scanner_obj.tokens.append(
                    Token("integer_divide", "", scanner_obj.line_num)
                )
                i += 2
            else:
                scanner_obj.tokens.append(Token("divide", "", scanner_obj.line_num))
                i += 1

        # Identifying modulus equal or modulus token
        elif source_code[i] == "%":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("modulus_equal", "", scanner_obj.line_num)
                )
                i += 2
            else:
                scanner_obj.tokens.append(Token("modulus", "", scanner_obj.line_num))
                i += 1

        # Identifying comma token
        elif source_code[i] == ",":
            scanner_obj.tokens.append(Token("comma", "", scanner_obj.line_num))
            i += 1

        # Identifying not_equal token
        elif source_code[i] == "!" and source_code[i + 1] == "=":
            scanner_obj.tokens.append(Token("not_equal", "", scanner_obj.line_num))
            i += 2

        # Identifying greater_than or greater than equal token
        elif source_code[i] == ">":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("greater_than_equal", "", scanner_obj.line_num)
                )
                i += 2
            else:
                scanner_obj.tokens.append(
                    Token("greater_than", "", scanner_obj.line_num)
                )
                i += 1

        # Identifying less than or less than equal to token
        elif source_code[i] == "<":
            if source_code[i + 1] == "=":
                scanner_obj.tokens.append(
                    Token("less_than_equal", "", scanner_obj.line_num)
                )
                i += 2
            else:
                scanner_obj.tokens.append(Token("less_than", "", scanner_obj.line_num))
                i += 1

        # Identifying the token left_bracket
        elif source_code[i] == "[":
            scanner_obj.tokens.append(
                Token("token_left_bracket", "", scanner_obj.line_num)
            )
            i += 1

        # Identifying the token right_bracket
        elif source_code[i] == "]":
            scanner_obj.tokens.append(
                Token("token_right_bracket", "", scanner_obj.line_num)
            )
            i += 1

        # If nothing is matched then increment the index
        else:
            i += 1

    # If indentLevel is not 0 then generate unindent tokens until indentLevel is zero
    if scanner_obj.indentLevel > 0:
        while scanner_obj.indentLevel != 0:
            token = Token("unindent", "", scanner_obj.line_num)
            scanner_obj.tokens.append(token)

            scanner_obj.indentLevel -= 1

    # Return the generated tokens
    return scanner_obj.tokens
