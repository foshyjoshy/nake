import brain

import numpy as np
import matplotlib.pyplot as plt


brain.BasicBrain

data = []
row_labels =[
    "abs moves to left board edge",
    "abs moves to top board edge",
    "abs moves to right board edge",
    "abs moves to bottom board edge",
    "moves to food X",
    "moves to food Y",
    "abs moved to self 0 degrees",
    "abs moved to self 45 degrees",
    "abs moved to self 90 degrees",
    "abs moved to self 135 degrees",
    "abs moved to self 180 degrees",
    "abs moved to self 225 degrees",
    "abs moved to self 270 degrees",
    "abs moved to self 315 degrees"]


data = np.arange(14)[...,None]

fig, axs =plt.subplots(1,2)
axs[0].axis('tight')
axs[0].axis('off')
the_table = axs[0].table(
    cellText=data,
    rowLabels=row_labels,
    colLabels=['',"inputs"],
    loc='center',
    rowLoc='right')

im = np.arange(10000).reshape((100,100))
axs[1].imshow(im)


fig.tight_layout()

plt.show()


