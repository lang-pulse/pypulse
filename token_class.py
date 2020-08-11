class Token:
    """
    Token class is responsible for creating tokens
    """

    def __init__(self, type, val, line_num):
        """
        Class initializer
        Params
        ======
        type     (string) = type of token as string
        val      (string) = value stored at token
        line_num (int)    = line number
        Values
        ======
        type     (string) = type of token as string
        typedig  (int)    = type of token as integer
        val      (string) = value stored at token
        line_num (int)    = line number
        """

        self.type = type
        self.val = val
        self.line_num = line_num

    def __str__(self):
        """
        Returns
        =======
        string: The string representation of Token object, which can be used to print the tokens
        """

        return "Token(%s, %s)" % (self.type, self.val)
