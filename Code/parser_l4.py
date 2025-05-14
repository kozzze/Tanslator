token_map = {
    "W1": "int", "W2": "char", "W3": "float", "W4": "double", "W5": "return",
    "W6": "if", "W7": "else", "W8": "for", "W9": "while", "W10": "do",
    "W11": "switch", "W12": "case", "W13": "break", "W14": "continue",
    "W15": "default", "W16": "void", "W17": "static", "W18": "struct",
    "W19": "typedef", "W20": "union", "W21": "unsigned", "W22": "signed",
    "W23": "long", "W24": "short", "W25": "goto", "W26": "sizeof",
    "W27": "main", "W28": "printf", "W29": "scanf", "W30": "#include",

    "O1": "==", "O2": "!=", "O3": "<=", "O4": ">=", "O5": "&&", "O6": "||",
    "O7": "+=", "O8": "-=", "O9": "*=", "O10": "/=", "O11": "%=",
    "O12": "+", "O13": "-", "O14": "*", "O15": "/", "O16": "%",
    "O17": "=", "O18": "<", "O19": ">",

    "R1": "(", "R2": ")", "R3": "{", "R4": "}", "R5": "[", "R6": "]",
    "R7": ",", "R8": ";", "R9": ".",
}

def classify_token(value):
    if value in {"#", "include", "int", "main", "return", "printf", "scanf", "if"}:
        return "keyword"
    elif value.startswith('"'):
        return "str"
    elif value.isdigit():
        return "num"
    elif value in {"<", ">", "(", ")", "{", "}", ";", ",", ".", "=",
                   "==", "!=", "<=", ">=", "+", "-", "*", "/", "%"}:
        return "symbol"
    else:
        return "id"

class Token:
    def __init__(self, line, code):
        self.line = line
        self.code = code
        self.lexeme = token_map.get(code, code)
        self.type = classify_token(self.lexeme)

    def __repr__(self):
        return f"{self.lexeme} ({self.type}) @ {self.line}"

class Tokenizer:
    def __init__(self, filename):
        self.tokens = self.load(filename)
        self.pos = 0

    def load(self, filename):
        tokens = []
        with open(filename, "r") as f:
            for lineno, line in enumerate(f, 1):
                for code in line.strip().split():
                    tokens.append(Token(lineno, code))
        return tokens

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        self.pos += 1

    def expect(self, lexeme=None, type_=None):
        tok = self.current()
        if not tok:
            raise SyntaxError("Ожидался токен, но достигнут конец файла")
        if lexeme and tok.lexeme != lexeme:
            raise SyntaxError(f"[Строка {tok.line + 1}] Ожидалось '{lexeme}', найдено '{tok.lexeme}'")
        if type_:
            if isinstance(type_, str) and tok.type != type_:
                raise SyntaxError(f"[Строка {tok.line + 1}] Ожидался тип '{type_}', найдено '{tok.type}'")
            if isinstance(type_, set) and tok.type not in type_:
                raise SyntaxError(f"[Строка {tok.line + 1}] Ожидался один из типов {type_}, найдено '{tok.type}'")
        self.next()
        return tok

class SyntaxAnalyzer:
    def __init__(self, tokenizer):
        self.tok = tokenizer

    def parse(self):
        self.parse_program()
        print("Синтаксический анализ завершён без ошибок")

    def parse_program(self):
        self.parse_includes()
        self.parse_main()

    def parse_includes(self):
        while self.tok.current() and self.tok.current().lexeme == "#include":
            self.tok.expect("#include")
            self.tok.expect("<")
            self.tok.expect(None, {"id", "num"})
            self.tok.expect(">")

    def parse_main(self):
        self.tok.expect("int")
        self.tok.expect("main")
        self.tok.expect("(")
        self.tok.expect(")")
        self.tok.expect("{")
        self.parse_statements()
        self.tok.expect("}")

    def parse_statements(self):
        while self.tok.current() and self.tok.current().lexeme != "}":
            self.parse_statement()

    def parse_declaration(self):
        self.tok.expect("int")
        self.tok.expect(None, "id")
        self.tok.expect("=")
        self.tok.expect(None, {"num", "id"})
        self.tok.expect(";")

    def parse_statement(self):
        current = self.tok.current()
        if current.lexeme == "int":
            self.parse_declaration()
        elif current.lexeme == "printf":
            self.tok.expect("printf")
            self.tok.expect("(")
            self.tok.expect(None, "str")
            self.tok.expect(")")
            self.tok.expect(";")
        elif current.lexeme == "return":
            self.tok.expect("return")
            self.tok.expect(None, {"num", "id"})
            self.tok.expect(";")
        elif current.lexeme == "if":
            self.parse_if()
        elif current.lexeme == "while":
            self.parse_while()

        else:
            raise SyntaxError(f"[Строка {current.line}] Неожиданный токен: '{current.lexeme}'")

    def parse_if(self):
        self.tok.expect("if")
        self.tok.expect("(")
        self.tok.expect(None, {"id", "num"})
        self.tok.expect("+")
        self.tok.expect(None, {"id", "num"})
        self.tok.expect("==")
        self.tok.expect(None, {"id", "num"})
        self.tok.expect(")")
        self.tok.expect("return")
        self.tok.expect(None, {"num", "id"})
        self.tok.expect(";")

    def parse_while(self):
        self.tok.expect("while")
        self.tok.expect("(")
        self.tok.expect(None, {"id", "num"})
        self.tok.expect("<")
        self.tok.expect(None, {"id", "num"})
        self.tok.expect(")")
        self.tok.expect("{")
        self.parse_statements()
        self.tok.expect("}")

if __name__ == "__main__":
    try:
        tokenizer = Tokenizer("tokens_output.txt")
        analyzer = SyntaxAnalyzer(tokenizer)
        analyzer.parse()
    except SyntaxError as e:
        print("Синтаксическая ошибка:")
        print(e)