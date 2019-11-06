#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

dpi = 96
plt.figure(figsize=(800/dpi, 800/dpi), dpi=dpi)

conn = sqlite3.connect("stats.sqlite")
c = conn.cursor()
c.execute('SELECT students FROM classrooms')
X = [ r[0] for r in c.fetchall() ]
conn.close()


num_bins = 21
mu = np.mean(X)
sigma = np.std(X)

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(X, num_bins, density=1)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(bins, y, '--')
ax.set_xticks(range(np.min(X), np.max(X), 2))
ax.set_xlabel("Students per Classroom")
ax.set_ylabel("Probability density")
ax.set_title("Students per Classroom Histogram")

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()


fig.savefig("./artifacts/students-per-classroom-histogram.png", dpi=dpi)
