w = 4 ** 511 + 2 ** 511 - 511
q = ''
while w:
    q += str(w % 2)
    w = w // 2
print(q.count('1'))
