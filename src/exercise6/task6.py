import json

def merge_proc(d):
    merged_list = []
    for i in d:
        merged_list += d[i]
    return sorted(merged_list, key=lambda x: x['year'])

with open("input.txt", "r") as f_in:
    try:
        data = json.load(f_in)
    except ValueError as err:
        print('Incorrect input')
        exit(1)

res = {'list0': merge_proc(data)}

with open("output.json", "w") as f_out:
    json.dump(res, f_out, indent = 4)