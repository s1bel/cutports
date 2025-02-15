import itertools

s1 = range(1,100)
s2 = {4, 5, 6, 7, 80, 82}

print()




def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]

print(list(ranges(list(set(s1) - set(s2)))))