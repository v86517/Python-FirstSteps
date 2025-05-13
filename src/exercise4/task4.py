def pascal_triangle(N):
    for i in range(N):
        binom = 1
        #print(' '*(N-i), end='')
        for j in range(0, i + 1):
            print(binom, end=' ')
            binom = binom * (i - j) // (j + 1)
        print()

N = input().strip()
if N.isdigit() and int(N) > 0:
    N = int(N)
    pascal_triangle(N)
else:
    print("Natural number was expected")