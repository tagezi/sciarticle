str = '1.23,2.4,3.123'
total = 0
ar = str.split(',')
print(ar)
print(len(ar))

for i in range(0, len(ar)):
    total = total + float(ar[i])

print(total)