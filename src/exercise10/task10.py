def req_input():
    try:
        dev_list_len, work_time = map(int, input().split())
    except Exception as err:
        print(err)
        exit(1)

    if dev_list_len <= 0 or work_time < 0:
        print('Incorrect request input')
        exit(1)
    return dev_list_len, work_time

def get_input_data(n):
    try:
        list_input = [list(map(int, input().split())) for _ in range(n)]
    except Exception as err:
        print(err)
        exit(1)

    for item in list_input:
        if (1000 >= item[0] >= 10000) or item[1]<0 or item[2]<0:
            print('Incorrect devices data')
            exit(1)
    return list_input

def proc_input(l, t):
    l.sort(key=lambda x: x[0])
    filtered_dict = dict()
    for i in range(len(l)):
        if l[i][0] not in filtered_dict.keys():
            if (i != (len(l)-1) and l[i+1][0] == l[i][0]) and l[i][2]<=t:
                filtered_dict[l[i][0]] = [[l[i][1], l[i][2]]]
        else:
            filtered_dict[l[i][0]].append([l[i][1], l[i][2]])

    for key, value in filtered_dict.items():
        filtered_dict[key] = sorted(value, key=lambda item: item[0])

    prices = []
    for value in filtered_dict.values():
        prices.append(value[0][0] + value[1][0])

    return prices

devices_list_len, dev_time_request = req_input()
dev_list_input = get_input_data(devices_list_len)
list_prices = proc_input(dev_list_input, dev_time_request)
print(min(list_prices))