import re

# Приоритет операторов
OPERATOR_PRIORITY = {
    "=": 1,
    "||": 2, "&&": 3,
    "<": 4, "<=": 4, ">": 4, ">=": 4, "==": 4, "!=": 4,
    "+": 5, "-": 5,
    "*": 6, "/": 6, "%": 6,
    "(": 0, ")": 0, "[": -1, "]": -1  # Учитываем скобки массивов
}

# Функция перевода в ОПЗ (алгоритм Дейкстры)
def to_opz(expression_tokens):
    output = []
    stack = []

    for token in expression_tokens:
        if token.isalnum():  # Переменная или число
            output.append(token)
        elif token in ["(", "["]:  # Открывающая скобка
            stack.append(token)
        elif token in [")", "]"]:  # Закрывающая скобка
            while stack and stack[-1] not in ["(", "["]:
                output.append(stack.pop())  # Выталкиваем всё до `(` или `[`
            if stack and stack[-1] in ["(", "["]:
                stack.pop()  # Убираем `(` или `[`, не добавляя в ОПЗ
        elif token in OPERATOR_PRIORITY:  # Оператор
            while stack and stack[-1] not in ["(", "["] and OPERATOR_PRIORITY[stack[-1]] >= OPERATOR_PRIORITY[token]:
                output.append(stack.pop())
            stack.append(token)

    while stack:  # Выталкиваем остатки из стека
        output.append(stack.pop())

    return output


# Функция обработки `if`, учитывая вложенные скобки
def process_if_statement(expression):
    expression = expression.replace("(", " ( ").replace(")", " ) ")
    tokens = expression.split()
    opz_condition = to_opz(tokens)  # Переводим в ОПЗ
    return " ".join(opz_condition) + " УПЛ"


# Функция обработки `while`
def process_while_statement(expression):
    expression = expression.replace("(", " ( ").replace(")", " ) ")
    tokens = expression.split()
    opz_condition = to_opz(tokens)  # Переводим в ОПЗ
    return " ".join(opz_condition) + " УЦ"  # УЦ - Условный Цикл


# Функция обработки `for`, чтобы преобразовать в ОПЗ
def process_for_statement(expression, loop_body):
    expression = expression.replace("(", " ( ").replace(")", " ) ")
    tokens = expression.split(";")

    if len(tokens) != 3:
        return "Ошибка в синтаксисе for"

    init_part = to_opz(tokens[0].split())  # `i = 0`
    condition_part = to_opz(tokens[1].split())  # `i < 10`
    increment_part = to_opz(tokens[2].split())  # `i = i + 1`

    result = [
        " ".join(init_part),  # Инициализация (выполняется один раз)
        " ".join(condition_part) + " УЦ"  # Проверка условия перед каждой итерацией
    ]

    # Добавляем тело цикла перед инкрементом
    result.extend(loop_body)

    # Добавляем инкремент перед возвратом к проверке условия
    result.append(" ".join(increment_part))

    # Условный переход к проверке условия
    result.append("УЦ")

    return "\n".join(result)
# Основная функция обработки кода
def convert_to_opz_plain(code_lines):
    result = []
    i = 0
    while i < len(code_lines):
        line = code_lines[i].strip()

        if line in ["{", "}"]:  # Игнорируем фигурные скобки
            i += 1
            continue

        if line.startswith("if"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            result.append(process_if_statement(condition))
            i += 1
            continue

        if line.startswith("while"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            result.append(process_while_statement(condition))
            i += 1
            continue

        if line.startswith("for"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            loop_body = []
            i += 1

            # Собираем тело цикла
            while i < len(code_lines) and code_lines[i].strip() != "}":
                loop_body.append(code_lines[i].strip())
                i += 1

            processed_body = convert_to_opz_plain(loop_body)  # Преобразуем тело цикла
            result.append(process_for_statement(condition, processed_body))
            i += 1
            continue

        if "=" in line:
            var_name, expr = line.split("=")
            var_name = var_name.strip()
            expr = expr.strip().rstrip(";")
            expr = expr.replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ")
            expr_tokens = expr.split()
            opz_expr = to_opz(expr_tokens)
            result.append(f"{var_name} {' '.join(opz_expr)} =")
            i += 1
            continue

        if "[" in line and "]" in line:
            array_access = line.replace("[", " [ ").replace("]", " ] ").split()
            opz_expr = to_opz(array_access)
            result.append(" ".join(opz_expr))
            i += 1
            continue

        i += 1

    return result

# Пример кода
code_example = [
    "if ((a - b) > 8) {",
    "    while ((a + b) < 20) {",
    "        x = arr[i] + 3;",
    "    }",
    "    for (i = 0; i < 10; i = i + 1) {",
    "        y = b[i] * 2;",
    "    }",
    "}"
]

# Выполняем обработку кода
opz_result = convert_to_opz_plain(code_example)

# Вывод результата
for line in opz_result:
    print(line)