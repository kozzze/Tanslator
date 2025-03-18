import re

OPERATOR_PRIORITY = {
    "=": 1,
    "||": 2, "&&": 3,
    "<": 4, "<=": 4, ">": 4, ">=": 4, "==": 4, "!=": 4,
    "+": 5, "-": 5,
    "*": 6, "/": 6, "%": 6,
    "(": 0, ")": 0, "[": -1, "]": -1
}

def to_opz(expression_tokens):
    output = []
    stack = []

    for token in expression_tokens:
        if token.isalnum() or "АЭМ" in token:
            output.append(token)
        elif token in ["(", "["]:
            stack.append(token)
        elif token in [")", "]"]:
            while stack and stack[-1] not in ["(", "["]:
                output.append(stack.pop())
            if stack and stack[-1] in ["(", "["]:
                stack.pop()
        elif token in OPERATOR_PRIORITY:
            while stack and stack[-1] not in ["(", "["] and OPERATOR_PRIORITY[stack[-1]] >= OPERATOR_PRIORITY[token]:
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output

def process_array_access(expression):
    tokens = expression.replace("[", " [ ").replace("]", " ] ").split()
    output = []
    i = 0

    while i < len(tokens):
        if i < len(tokens) - 2 and tokens[i + 1] == "[":
            array_name = tokens[i]
            index_expr = [tokens[i + 2]]
            index_opz = to_opz(index_expr)
            array_access_opz = [array_name] + index_opz + ["1 АЭМ"]
            output.extend(array_access_opz)  # Добавляем массив как цельный операнд
            i += 3
        elif tokens[i] != "]":
            output.append(tokens[i])
        i += 1

    return output

def process_if_statement(expression):
    return " ".join(to_opz(expression.split())) + " УПЛ"

def process_while_statement(expression):
    return " ".join(to_opz(expression.split())) + " УЦ"

def convert_to_opz_plain(code_lines):
    result = []
    i = 0
    while i < len(code_lines):
        line = code_lines[i].strip()

        if line in ["{", "}"]:  # Игнорируем фигурные скобки
            i += 1
            continue

        # Обрабатываем `if`
        if line.startswith("if"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            tokens = condition.replace("(", " ( ").replace(")", " ) ").split()
            result.append(" ".join(to_opz(tokens)) + " УПЛ")
            i += 1
            continue

        # Обрабатываем `while`
        if line.startswith("while"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            tokens = condition.replace("(", " ( ").replace(")", " ) ").split()
            result.append(" ".join(to_opz(tokens)) + " УЦ")
            i += 1
            continue

        # Обрабатываем `for`
        if line.startswith("for"):
            condition = line[line.index("(") + 1: line.rindex(")")]
            tokens = condition.split(";")

            if len(tokens) != 3:
                result.append("Ошибка в синтаксисе for")
                i += 1
                continue

            init_part = to_opz(tokens[0].split())  # `i = 0`
            condition_part = to_opz(tokens[1].split())  # `i < 10`
            increment_part = to_opz(tokens[2].split())  # `i = i + 1`

            result.append(f"{' '.join(init_part)}")
            result.append(f"{' '.join(condition_part)} УЦ")

            loop_body = []
            i += 1

            while i < len(code_lines) and code_lines[i].strip() != "}":
                loop_body.append(code_lines[i].strip())
                i += 1

            processed_body = convert_to_opz_plain(loop_body)
            result.extend(processed_body)

            result.append(f"{' '.join(increment_part)}")
            result.append("УЦ")

            i += 1
            continue

        # Обрабатываем присваивание
        if "=" in line:
            if line.count("=") > 1 and "==" not in line:
                var_name, expr = line.split("=", 1)  # Разделяем только по первому `=`
            else:
                var_name, expr = line.split("=")

            var_name = var_name.strip()
            expr = expr.strip().rstrip(";")

            if "[" in var_name and "]" in var_name:
                var_name = " ".join(process_array_access(var_name))  # Обрабатываем массив

            expr_tokens = process_array_access(expr)  # Получаем список токенов
            expr_tokens = to_opz(expr_tokens)  # Пропускаем через ОПЗ

            result.append(f"{var_name} {' '.join(expr_tokens)} =")
            i += 1
            continue

        # Обрабатываем обращение к массиву без присваивания
        if "[" in line and "]" in line:
            array_tokens = process_array_access(line)
            result.append(" ".join(array_tokens))
            i += 1
            continue

        i += 1

    return result

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

opz_result = convert_to_opz_plain(code_example)

for line in opz_result:
    print(line)