a = [1, 5, 3, 8, 4, 9, 7]
flag = True
while flag:
    flag = False
    for i in range(len(a) - 1):
        if a[i] > a [i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            print(a)
            flag = True
