import timeit


setups = "histogram = {}"

s = """\
for i in range(5, 0, -1):
	histogram[i] = 5 - i
"""

s2 = """\
for i in range(5):
	histogram[5 - i] = i
"""

print timeit.timeit(stmt=s, setup=setups, number=100000)
print timeit.timeit(stmt=s2, setup=setups, number=100000)
