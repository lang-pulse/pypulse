class Scanner:
    def __init__(self):
        self.tokens = []
        self.line_num = 1
        self.isIndent = False
        self.isUnindent = False
        self.indentLevel = 0
        self.unindentLevel = 0
