import sys

with open(sys.argv[1]) as f:
    values = [ int(line) for line in f.readlines() ]


lines = values
n = 0
last = 1e50
for line in lines:
    new = int(line)
    if new > last:
        n += 1
    last = new

print(n)



n = 0
for i in range(3, len(values)):
    s_prev = sum(values[i - 3: i])
    s_new = sum(values[i - 2: i + 1])
    if s_new > s_prev:
        n += 1

print(n)
