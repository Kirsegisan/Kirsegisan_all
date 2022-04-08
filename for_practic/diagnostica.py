T = [0, 0, 1, 1, 1, 1]
for i in range(6, 73):
    T.append(T[i - 1])
    if i % 3 == 0:
        T[i] += T[i // 3]
    if i == 24:
        T[i] = 0
    print(T)
