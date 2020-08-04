import matplotlib.pyplot as plt

# Function called from main, separated for easier debugging
def n_bodies():

    class Object():
        size = 0            # nr of all objects
        system = []         # array w/ references to all objects
        def __init__(self):
            self.x_hist_data = []
            self.y_hist_data = []
            self.r = [0, 0]         # position
            self.v = [0, 0]         # velocity
            self.a = [0, 0]         # acceleration
            self.m = 0              # mass
            self.__class__.size += 1
            self.__class__.system.append(self)
        @classmethod
        def initialize_accelerations(cls):
            """ Set acceleration vector for all objects base on current state of the system. """
            for o in cls.system:
                o.a = totalAccVector(Object.system, Object.system.index(o))


    def twoNorm(coordset):
        """ Euclidean magnitude of a vector. """
        res = 0
        for coord in coordset:
            res += coord**2
        return res**0.5

    def makeUnit(coordset):
        """ Normalize vector. """
        mag = twoNorm(coordset)
        return [coord / mag for coord in coordset]

    def diffVector(cs1, cs2):
        """ Vector cs1-cs2, pointing from cs2 to cs1. """
        return [cs1[i] - cs2[i] for i in range(len(cs1))]

    def euclidDist(cs1, cs2):
        """ Euclidean distance of two vectors. """
        return twoNorm(diffVector(cs1, cs2))

    def gAcc(cs1, cs2, m1):
        # acting ON cs2
        """ Gravitational acceleration acting on an object at position cs2 exerted by object cs1 of mass m1. 
            Params:
                cs1 {list of floats}    --  vector position of actor
                cs2 {list of floats}    --  vector positon of actee
                m1  {float}             --  mass of actor

            Return:
                {list of floats}    -- acceleration vector
        """  
        diff = diffVector(cs1, cs2)     # corrdset cs2 pulled towards cs1
        mag  = m1 / twoNorm(diff)**2    # force magnitude
        diff = makeUnit(diff)           # unit vector in the direction of force
        return [diff_elem * mag for diff_elem in diff] 



    def totalAccVector(system, current_index):
        """Return total acceleration vector on an object within a system.

        Arguments:
            system {list of Objects}    -- state monitoring list of the Object class
            current_index {int}         -- index of the current object within the system

        Returns:
            {list of floats} -- total acceleration vector on Object.system[current_index]
        """
        res = [0, 0]    # result
        part = []       # partial accelerations
        for index in range(Object.size):
            if index == current_index:    # no effect on self
                continue
            else:
                part.append(    # append acceleration from one
                    gAcc(                
                        system[index].r,
                        system[current_index].r,
                        system[index].m
                        ))
            for p in part:      # add up partials
                res[0] += p[0]
                res[1] += p[1]
        return res

    def step(o, delta):
        """Calculates dynamics of object o for each iteration of magnitude delta.

        Arguments:
            o {Object instance} -- object within the system
            delta {float}       -- size of iteration: the smaller it is, the more reslistic the simulation becomes
        """
        o.a = totalAccVector(Object.system, Object.system.index(o))
        o.r[0] = o.v[0] * delta + o.r[0] 
        o.r[1] = o.v[1] * delta + o.r[1]
        o.v[0] = o.a[0] * delta + o.v[0] 
        o.v[1] = o.a[1] * delta + o.v[1] 


    # Initialize objects here
    o1 = Object()
    o1.r = [0, 0]
    o1.v = [0, 0]
    o1.m = 100
    
    o2 = Object()
    o2.r = [20, 0]
    o2.v = [0, 2.23606798]
    o2.m = 0.001

    o3 = Object()
    o3.r = [10.5, 0]
    o3.v = [0, -3.162277]
    o3.m = 0.001

    o4 = Object()
    o4.r = [15.3, 0]
    o4.v = [0, 3]
    o4.m = 0.5

    o5 = Object()
    o5.r = [25, 0]
    o5.v = [0, 4.5]
    o5.m = 0.0000001

    Object.initialize_accelerations()
    # End of object initialization

    t = 0               # time
    delta = 0.001      # iteration time step
    total_time = 100    # total time simulated

    # add initial positions to object history
    for o in Object.system:
        o.x_hist_data.append(o.r[0])
        o.y_hist_data.append(o.r[1])

    import time
    start = time.time()

    i = 0   # iteration counter
    # This is the simulation loop here
    # Just records histories and take time steps
    while i < (total_time/delta):
        t = i * delta
        for o in Object.system:
            # Only record part of the history,
            # we'll have way more than what we need for plotting
            if i % 20 == 0:  
                o.x_hist_data.append(o.r[0])
                o.y_hist_data.append(o.r[1])
            step(o, delta)
        i += 1

    end = time.time()
    print(f"Total time of simulation: {end-start} seconds.")

    # Created a static plot of full object paths.
    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1)
    for o in Object.system:
        plt.plot(o.x_hist_data, o.y_hist_data)
    plt.show()

    # Create animation
    from matplotlib.animation import FuncAnimation
    import math

    # Figure
    fig = plt.figure()
    # Axes object
    ax  = fig.add_subplot(1, 1, 1)
    ax.set_xlim((-30,30))
    ax.set_ylim((-30,30))
    # We restrict to 2D here.
    plot_data = [[[], []] for o in range(Object.size)]  # the data for each object
    plot_object = [[] for o in range(Object.size)]      # the plot matplotlib returns for each object
    for i in range(Object.size):
        plot_object[i], = ax.plot(plot_data[i][0], plot_data[i][1]) # create plot objects

    # Initialize plot objects with empty data
    def init():
        for plot in plot_object:
            plot.set_data([], [])
        return plot_object

    # Constrains of this func are
    # name: update
    # single param: index_to_add=FRAME_NUMBER
    # return: plot object or (in this case), list of plot objects
    def update(index_to_add):
        # Empty the plot history!
        plot_history = [[[], []] for o in range(Object.size)]   
        # Plot only last 100 entries
        # Set last 100 to be [base:index_to_add]
        base = 0
        if index_to_add > 100:
            base = index_to_add - 100
        # This is the actual plotting:
        for i in range(Object.size):    # for each object
            o = Object.system[i]        # select it
            # Specify the hisoty we want to use:  [partial_x_hist, partial_y_hist]
            plot_history[i] = [o.x_hist_data[base:index_to_add], o.y_hist_data[base:index_to_add]]
            # Finally set data for the frame!
            plot_object[i].set_data(plot_history[i][0], plot_history[i][1])
        return plot_object
    
    ani = FuncAnimation(fig, update, frames=list(range(len(Object.system[0].x_hist_data))), init_func=init, blit=True, interval=10)
    plt.show()



# MAIN
if __name__ == "__main__":
    n_bodies()