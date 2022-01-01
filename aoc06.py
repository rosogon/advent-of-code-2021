import sys
from collections import defaultdict


def read_file(path):
    with open(path) as f:
        line = f.readline()
        timers = [int(n) for n in line.split(",")]
    result = defaultdict(int)
    for t in timers:
        result[t] += 1
        
    return result


def timers_str(timers):
    return ','.join(str(t) for t in timers)


def next_day(timers):
    for i in range(len(timers)):
        t = timers[i]
        if t == 0:
            new_t = 6
            timers.append(8)
        else:
            new_t = t - 1
        timers[i] = new_t
    return timers


def next_day_2(timers):
    new_timers = defaultdict(int)
    new_timers[6] = timers[0]
    new_timers[8] = timers[0]
    for i in range(0, 8):
        new_timers[i] += timers[i+1]
    return new_timers


def next_day_3(timers):
    head = timers.pop(0)
    timers[6] += head
    timers.append(head)
    return timers


def main():
    debug = False
    timers = read_file(sys.argv[1])
    
##    for i in range(1, int(sys.argv[2]) + 1):
##        timers = next_day_2(timers)
##    print(sum(timers.values()))

    timers = [timers[i] for i in range(0, 9)]
    for i in range(0, int(sys.argv[2])):
        timers = next_day_3(timers)
    print(sum(timers))
    
          
if __name__ == "__main__":
    main()
