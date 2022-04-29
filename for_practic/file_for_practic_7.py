q = [0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2]
for n in range(11, 32):
    q.append(q[n - 1] + (q[n // 4] if not n % 4 and n // 4 >= 10 else 0))
    print(q)