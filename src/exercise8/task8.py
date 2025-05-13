N = int(input())
list_in = []
list_unique = []

for i in range(N):
    list_in.append(int(input()))

for i in list_in:
    if i in list_unique:
        continue
    else:
        list_unique.append(i)

print(len(list_unique))