import re

# Приоритет операторов
OPERATOR_PRIORITY = {
    "=": 1,
    "||": 2, "&&": 3,
    "<": 4, "<=":4, ">": 4, ">=":4, "==": 4, "!=": 4,
"+": 5, "-": 5,
"*": 6, "/": 6, "%": 6,
"(": 0, ")": 0
}

# Функция перевода в ОПЗ (алгоритм Дейкстры)
def to_opz(expression_tokens):
    output = []
    stack = []

    for token in expression_tokens:
        if token.isalnum():  # Переменная или число
            output.append(token)
        elif token == "(":  # Открывающая скобка
            stack.append(token)
        elif token == ")":  # Закрывающая скобка
            while stack and stack[-1] != "(":
                output.append(stack.pop())  # Выталкиваем всё до `(`
            if stack and stack[-1] == "(":
                stack.pop()  # Убираем `(`, не добавляя в ОПЗ
        elif token in OPERATOR_PRIORITY:  # Оператор
            while stack and stack[-1] != "(" and OPERATOR_PRIORITY[stack[-1]] >= OPERATOR_PRIORITY[token]:
                output.append(stack.pop())
            stack.append(token)

    while stack:  # Выталкиваем остатки из стека
        output.append(stack.pop())

    return output


# Функция обработки `if`, учитывая вложенные скобки
def process_if_statement(expression):
    # Добавляем пробелы вокруг скобок, чтобы `split()` работал правильно
    expression = expression.replace("(", " ( ").replace(")", " ) ")
    tokens = expression.split()
    opz_condition = to_opz(tokens)  # Переводим в ОПЗ
    return " ".join(opz_condition) + " УПЛ"


# Основная функция обработки кода
def convert_to_opz_plain(code_lines):
    result = []
    for line in code_lines:
        line = line.strip()

        # Убираем `{}` перед обработкой
        if line in ["{", "}"]:
            continue

        # Обрабатываем `if`
        if line.startswith("if"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            result.append(process_if_statement(condition))
            continue

        # Обрабатываем присваивание
        if "=" in line:
            var_name, expr = line.split("=")
            var_name = var_name.strip()
            expr = expr.strip().rstrip(";")

            # Разделяем токены правильно (добавляем пробелы)
            expr = expr.replace("(", " ( ").replace(")", " ) ")
            expr_tokens = expr.split()

            opz_expr = to_opz(expr_tokens)
            result.append(f"{var_name} {' '.join(opz_expr)} =")
            continue

        result.append(line)

    return result

code_example = [
  "if ((a - b) > 8) {",
  "if ((a + b) == 10){",
    "a[1];",
    "}"
]

opz_result = convert_to_opz_plain(code_example)

for line in opz_result:
    print(line)

    ## оператор цикла с предусловием и обращение к массивам обрабатывать