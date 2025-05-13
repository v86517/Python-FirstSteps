def print_m(m):
    for i in m:
        print(*i)

def check_square(m, i, j):
    res = False
    #if i != len(m) and j != 0:
    if j != 0:
        if m[i][j-1] == 0 and m[i+1][j-1] == 0 and m[i+1][j] != 0:
            res = True
    else:
        res = True
    return res

def proc_square(m, i, j):
    cnt = 0
    for x in range(j, len(m[0])):
        if m[i][x] == 1:
            cnt+=1
        else:
            break

    for k in range(i,i+cnt):
        for l in range(j,j+cnt):
            m[k][l] = 0

def proc_circle(m, i, j):
    cnt = 0
    while j != len(m[0]) and m[i][j] == 1:
        cnt+=1
        m[i][j] = 0
        if (j+1 == len(m[0]) or m[i][j+1] == 0) and i+1 != len(m):
            if m[i+1][j-cnt] == 0:
                if m[i+1][j-cnt+1] == 0:
                    j = j-cnt+2
                else:
                    j = j-cnt+1
                i+=1
                cnt = 0
                break
            else:
               i+=1
               j-=cnt
               cnt = 0
        else:
            j+=1
    while j != len(m[0]) and m[i][j] == 1:
        cnt+=1
        m[i][j] = 0
        if (j+1 == len(m[0]) or m[i][j+1] == 0) and i+1 != len(m):
            i+=1
            j=j-cnt+2
        else:
            j+=1


with open('f_in.txt', 'r') as f_in:
    m = [[int(num) for num in line.split()] for line in f_in]
#print_m(m)

circle = 0
square = 0
for i in range(len(m)-1):
    for j in range(len(m[0])-1):
        if m[i][j] == 1:
            if check_square(m,i,j):
                proc_square(m, i, j)
                square += 1
            else:
                proc_circle(m, i, j)
                circle+=1
#print_m(m)
print(square,circle)
#0 0 0 0 0 0 0 0 1 0;0 1 1 1 0 0 0 1 1 1;0 1 1 1 0 0 0 0 1 0;0 1 1 1 0 0 0 0 0 0;0 0 0 0 0 0 0 0 0 0;0 1 1 0 0 1 1 0 0 0;0 1 1 0 1 1 1 1 0 0;0 0 0 0 1 1 1 1 0 0;1 1 0 0 0 1 1 0 0 0;1 1 0 0 0 0 0 0 0 0
#0 1 1 0 0 1 1 0 0 0;0 1 1 0 1 1 1 1 0 0;0 0 0 0 1 1 1 1 0 0;1 1 0 0 0 1 1 0 0 0;1 1 0 0 0 0 0 0 0 0
