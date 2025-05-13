v1= [float(i) for i in input().split()]
v2= [float(i) for i in input().split()]

res = 0
for i in range(len(v1)):
    res+=v1[i] * v2[i]
print(res)

#1.0 2.0 3.0
#4.0 5.0 6.0
#32.0
