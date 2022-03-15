import random
q = random.randint(512, 1023)
while True:
    for i in range(12):
        if i == 1:
            q = random.randint(512, 1023)
            print(bin(q))
        else:
            q = random.randint(512, 1023)
            print(bin(q), end=' ')
