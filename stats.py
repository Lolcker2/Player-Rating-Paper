import numpy as np
from scipy import stats

x = []
y = []

filename = "nonlog log"
with open(filename, "r") as data:
    for line in data.read().split('\n'):
        if(len(line)) < 2:
            continue

        line = line.split(',')
        x.append(int(line[0].strip()))
        y.append(int(line[1].strip()))


slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(x), np.array(y))

# 3. Calculate R^2
r_squared = r_value**2

print(f"Line Equation: y = {slope:.2f}x + {intercept:.2f}")
print(f"R^2 score: {r_squared:.4f}")
