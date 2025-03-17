import re

LEXEME_CLASSES = {
    "W": "Служебное слово",
    "I": "Идентификатор",
    "O": "Операция",
    "R": "Разделитель",
    "N": "Число",
    "C": "Константа"
}

KEYWORDS = {
    kw: f"W{idx}" for idx, kw in enumerate([
        "int", "char", "float", "double", "return", "if", "else",
        "for", "while", "do", "switch", "case", "break", "continue",
        "default", "void", "static", "struct", "typedef", "union",
        "unsigned", "signed", "long", "short", "goto", "sizeof",
        "main", "printf", "scanf", "#include"
    ], start=1)
}

OPERATORS = {
    op: f"O{idx}" for idx, op in enumerate([
        "==", "!=", "<=", ">=", "&&", "||", "+=", "-=", "*=", "/=", "%=",
        "+", "-", "*", "/", "%", "=", "<", ">"
    ], start=1)
}

DELIMITERS = {
    delim: f"R{idx}" for idx, delim in enumerate([
        "(", ")", "{", "}", "[", "]", ",", ";", "."
    ], start=1)
}

TOKEN_PATTERNS = [
    (r'//.*', 'COMMENT'),
    (r'/\*.*?\*/', 'COMMENT', re.DOTALL),
    (r'#\s*include\s*<.*?>', 'W'),
    (r'\b(' + '|'.join(KEYWORDS.keys()) + r')\b', 'W'),
    (r'[a-zA-Z_]\w*', 'I'),
    (r'\d+\.\d+|\d+', 'N'),
    (r'".*?"', 'C'),
    (r'(' + '|'.join(map(re.escape, OPERATORS.keys())) + r')', 'O'),
    (r'(' + '|'.join(map(re.escape, DELIMITERS.keys())) + r')', 'R')
]

IDENTIFIERS = {}
ident_counter = 1
num_counter = 1
const_counter = 1

def tokenize(code):
    global ident_counter, num_counter, const_counter
    lines = code.split("\n")
    tokenized_lines = []

    for line in lines:
        tokens = []
        code = line.strip()
        while code:
            code = code.lstrip()
            match = None
            for pattern, lexeme_type, *flags in TOKEN_PATTERNS:
                regex_flags = flags[0] if flags else 0
                match = re.match(pattern, code, regex_flags)
                if match:
                    value = match.group(0)
                    if lexeme_type == "I":
                        if value in IDENTIFIERS:
                            lexeme_code = IDENTIFIERS[value]
                        else:
                            lexeme_code = f"I{ident_counter}"
                            IDENTIFIERS[value] = lexeme_code
                            ident_counter += 1
                    elif lexeme_type == "N":
                        lexeme_code = f"N{num_counter}"
                        num_counter += 1
                    elif lexeme_type == "C":
                        lexeme_code = f"C{const_counter}"
                        const_counter += 1
                    else:
                        lexeme_code = (
                            KEYWORDS.get(value, None) or
                            OPERATORS.get(value, None) or
                            DELIMITERS.get(value, None)
                        )

                    if lexeme_code:
                        tokens.append(lexeme_code)
                    code = code[len(value):]
                    break
            if not match:
                raise SyntaxError(f"Неизвестный символ: {code[:10]}")

        if tokens:
            tokenized_lines.append(" ".join(tokens))

    return tokenized_lines

# Читаем код из файла test.c
file_path = "test.c"

with open(file_path, "r", encoding="utf-8") as f:
    code_c = f.read()

# Запускаем лексический анализ
tokenized_lines = tokenize(code_c)

# Выводим и записываем результат
output_file = "tokens_output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for line in tokenized_lines:
        print(line)
        f.write(line + "\n")

print(f"\nЛексемы сохранены в файл {output_file}")