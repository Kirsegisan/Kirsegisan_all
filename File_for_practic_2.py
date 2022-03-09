import random
q = random.randint(1, 9999)
while True:
    for i in range(7):
        while True:
            if i != 1:
                q = random.randint(1, 9999)
                print(bin(q), end=' ')
            else:
                q += 1
                print(bin(q))

