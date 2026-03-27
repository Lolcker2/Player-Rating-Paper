# import numpy as np
import matplotlib.pyplot as plt
data = open('log').read().split('\n')
y = []
x = []
counter = 5
for item in data:
    if not item == '':
        item = item.split(',')
        x.append(int(item[0]))
        y.append(int(item[1]))

# std error, r^2 ...

# minimum_pair = (1300,748)
# maximum_pair = (1699,1239)
# new_x = [(itm - minimum_pair[0]) / (maximum_pair[0] - minimum_pair[0]) for itm in x]
# new_y = [(itm - minimum_pair[1]) / (maximum_pair[1] - minimum_pair[1]) for itm in y]
# plt.scatter(new_x, new_y)

plt.scatter(x, y)
plt.show()
