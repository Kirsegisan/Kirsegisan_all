import random
q = random.randint(512, 1023)
while True:
    for i in range(9):
        while True:
            if i != 1:
                q = random.randint(512, 1023)
                print(bin(q), end=' ')
            else:
                q += 1
                print(bin(q))

