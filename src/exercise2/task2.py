num = int(input())
res = True
if num < 0:
    res = False
else:
    dig_list = []
    while num > 0:
        dig_list.append(num % 10)
        num //= 10

    for i in range(len(dig_list) // 2):
        if dig_list[i] != dig_list[len(dig_list) - 1 - i]:
            res = False

print(res)
