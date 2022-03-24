def generate_numbers(n:int, m: int, prefix = None) -> None:
    """
    выводит в консоь перестоновки
    """
    if m == 0:
        print(prefix, end= ' ')
    else:
        prefix = prefix or []
        for digitals in range(n):
            if digitals in prefix:
                continue
            prefix.append(digitals)
            generate_numbers(n, m - 1, prefix)
            prefix.pop()


generate_numbers(int(input()), int(input()))
