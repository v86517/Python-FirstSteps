'''
def print_field(A):
    for i in range(N):
        for j in range(M):
            print((A[i][j]), end=' ')
        print()
'''
def fill_a(N, M):
    for i in range(N):
        A.append(list(map(int, input().split())))

def calc_b(N, M):
    B = [[0] * M] * N
    B[0][0] = A[0][0]
    for j in range(1, M):
        B[0][j] = A[0][j - 1] + A[0][j]

    for i in range(1, N):
        B[i][0] = A[i - 1][0] + A[i][0]

    for i in range(1, N):
        for j in range(1, M):
            B[i][j] = A[i][j] + max(B[i - 1][j], B[i][j - 1])
    return B[N - 1][M - 1]

N, M = [int(x) for x in input().split()]
A = []
fill_a(N, M)
res = calc_b(N, M)
print(res)