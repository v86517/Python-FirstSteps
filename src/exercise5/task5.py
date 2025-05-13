def plus_minus_check(s):
    neg = False
    if s[0] in '-+':
        if s[0] == '-':
            neg = True
        s = s[1:]
    return s, neg

def proc(s, int_or_frac):
    dic = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, }
    res = 0
    for i in range(len(s)):
        tmp = dic.get(s[i], -1)
        if tmp == -1:
            print('incorrect input')
            exit(1)
        else:
            if int_or_frac == True:
                tmp = tmp * (10 ** (len(s) - 1 - i))
            else:
                tmp = tmp / (10 ** (i + 1))
            res += tmp
    return res

str_in = input()
str_in, negative = plus_minus_check(str_in)
int_part, frac_part = str_in.split('.')
res_int = proc(int_part, True)
res_frac = proc(frac_part, False)
result = res_int+res_frac if negative==False else -(res_int+res_frac)
#print(result*2)
print(f"{(result*2):.3f}")