def matr(n):
    print(f'низ матрешки {bin(n)}')
    if n > 1:
        matr(n - 1)
    print(f'верх матрешки{bin(n)}')


if __name__ == '__main__':
    matr(int(input()))