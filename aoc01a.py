with open("01_input") as f:
    lines = f.readlines()

n = 0
last = 1e50
for line in lines:
    new = int(line)
    if new > last:
        n += 1
    last = new

print(n)
