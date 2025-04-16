import re

# Операции и ключевые слова
binary_ops = {'+': '+', '-': '-', '*': '*', '/': '/', '<': '<', '>': '>', '==': '=='}
commands = {'АЭМ': 'ARRAY_ACCESS', '=': 'ASSIGN', 'УПЛ': 'IF_COND', 'УЦ': 'CTRL_FLOW'}

# Простейший стековый интерпретатор OPЗ для восстановления C++ кода
class OPZParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.output = []
        self.stack = []
        self.indent_level = 0
        self.loop_context = []

    def indent(self):
        return '    ' * self.indent_level

    def parse(self):
        # Добавим стандартные заголовки C++
        self.output.append("#include <iostream>")
        self.output.append("using namespace std;")
        self.output.append("int main() {")
        self.indent_level += 1

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token in binary_ops:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(f'({a} {binary_ops[token]} {b})')
            elif token == 'АЭМ':
                index = self.stack.pop()
                array = self.stack.pop()
                self.stack.append(f'{array}[{index}]')
            elif token == '=':
                value = self.stack.pop()
                var = self.stack.pop()
                self.output.append(f'{self.indent()}{var} = {value};')
            elif token == 'УПЛ':
                condition = self.stack.pop()
                self.output.append(f'{self.indent()}if {condition} {{')
                self.indent_level += 1
            elif token == 'УЦ':
                # Разные случаи: while, for или конец блока
                if self.loop_context and self.loop_context[-1] == 'for':
                    self.indent_level -= 1
                    self.output.append(f'{self.indent()}}}')
                    self.loop_context.pop()
                elif self.stack:
                    condition = self.stack.pop()
                    self.output.append(f'{self.indent()}while {condition} {{')
                    self.indent_level += 1
                else:
                    self.indent_level -= 1
                    self.output.append(f'{self.indent()}}}')
            else:
                self.stack.append(token)
            self.pos += 1

        # Закрываем все открытые блоки
        while self.indent_level > 0:
            self.indent_level -= 1
            self.output.append(f'{self.indent()}}}')

        return self.output


def parse_opz(opz_lines):
    # Очистка и разбиение токенов по пробелам, пропуская заголовки
    tokens = []
    for line in opz_lines:
        line = line.strip()
        if not (line.startswith("#include") or line.startswith("using") or line.startswith("int main")):
            tokens.extend(line.split())
    parser = OPZParser(tokens)
    return parser.parse()


# Пример использования
opz_input = [
    "#include <iostream>",
    "using namespace std;",
    "int main()",
    "a b - 8 > УПЛ",
    "a b + 20 < УЦ",
    "x arr i АЭМ 3 + =",
    "i 0 =",
    "i 10 < УЦ",
    "y b i АЭМ 2 * =",
    "i i 1 + =",
    "УЦ"
]

cpp_lines = parse_opz(opz_input)
for line in cpp_lines:
    print(line)
