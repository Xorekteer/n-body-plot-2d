# What is this?

This is an n-body simulator written in python. Based on old c++ code.

Running the program generates a plot and and animation in matplotlib, showing the trajectory of all defined objects.

The new version:
 - relies on python-matplotlib for plotting
 - implements free dynamics (no constrained movement, no static bodies)
 - completely general (may define a large number of bodies)
 - automates the plotting process

# How to use it?

1. Install python3 and matplotlib.

`$pip install matplotlib`

2. Define your configuration of bodies in the source code. This should be straightforward.
 - initialize an instance of the class Object
 - define starting position and velocity
 - define starting mass

3. Run the program:

`$python3 simulator.py`

# What it looks like?

Clone the repo and see the demo folder.
