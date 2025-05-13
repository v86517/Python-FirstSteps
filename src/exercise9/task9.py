def calc_derivative(top_pow, coefficients, point):
    res = sum(coef_x * (top_pow - i) * point ** (top_pow - i - 1) for i, coef_x in enumerate(coefficients))
    return res

data_in = input().split()
n, x = int(data_in[0]), float(data_in[1])
coef_list = [float(input()) for _ in range(n + 1)]
der = calc_derivative(n, coef_list, x)
print(f'{der:.3f}')
