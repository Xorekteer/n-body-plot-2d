import matplotlib.pyplot as plt

def n_bodies():

    class Object():
        size = 0
        system = []
        def __init__(self):
            self.x_hist_data = []
            self.y_hist_data = []
            self.r = [0, 0]
            self.v = [0, 0]
            self.a = [0, 0]
            self.m = 0
            self.__class__.size += 1
            self.__class__.system.append(self)
        @classmethod
        def initialize_accelerations(cls):
            for o in cls.system:
                o.a = totalAccVector(Object.system, Object.system.index(o))



    def twoNorm(coordset):
        res = 0
        for coord in coordset:
            res += coord**2
        return res**0.5

    def makeUnit(coordset):
        mag = twoNorm(coordset)
        return [coord / mag for coord in coordset]

    def diffVector(cs1, cs2):
        return [cs1[i] - cs2[i] for i in range(len(cs1))]  #initialize diff

    def euclidDist(cs1, cs2):
        return twoNorm(diffVector(cs1, cs2))

    def gAcc(cs1, cs2, m1):
        # acting ON cs2
        diff = diffVector(cs1, cs2)
        mag  = m1 / twoNorm(diff)**2
        diff = makeUnit(diff)

        return [diff_elem * mag for diff_elem in diff]



    def totalAccVector(system, current_index):
        res = [0, 0]
        part = []
        for index in range(Object.size):
            if index == current_index:
                continue
            else:
                part.append(
                    gAcc(
                        system[index].r,
                        system[current_index].r,
                        system[index].m
                        ))
            for p in part:
                res[0] += p[0]
                res[1] += p[1]
        return res

    def step(o, delta):
        o.a = totalAccVector(Object.system, Object.system.index(o))
        o.r[0] = o.v[0] * delta + o.r[0] 
        o.r[1] = o.v[1] * delta + o.r[1]
        o.v[0] = o.a[0] * delta + o.v[0] 
        o.v[1] = o.a[1] * delta + o.v[1] 


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

    t = 0
    delta = 0.001
    i = 0

    for o in Object.system:
        o.x_hist_data.append(o.r[0])
        o.y_hist_data.append(o.r[1])

    while i < (100/delta):
        t = i * delta
        for o in Object.system:
            o.x_hist_data.append(o.r[0])
            o.y_hist_data.append(o.r[1])
            step(o, delta)
        i += 1 

    
    # cut down histories
    for o in Object.system:
        o.x_hist_data = [o.x_hist_data[elem] for elem in range(0, len(o.x_hist_data), 40)]
        o.y_hist_data = [o.y_hist_data[elem] for elem in range(0, len(o.y_hist_data), 40)]


    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1)
    for o in Object.system:
        plt.plot(o.x_hist_data, o.y_hist_data)
    plt.show()


    from matplotlib.animation import FuncAnimation
    import math

    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1)
    ax.set_xlim((-30,30))
    ax.set_ylim((-30,30))
    plot_data = [[[], []] for o in range(Object.size)]
    plot_object = [[] for o in range(Object.size)]
    for i in range(Object.size):
        plot_object[i], = ax.plot(plot_data[i][0], plot_data[i][1])

    def init():
        for plot in plot_object:
            plot.set_data([], [])
        return plot_object

    def update(index_to_add):
        base = 0
        if index_to_add > 100:
            base = index_to_add - 100
        plot_history = [[[], []] for o in range(Object.size)]
        for i in range(Object.size):
            o = Object.system[i]
            plot_history[i] = [o.x_hist_data[base:index_to_add], o.y_hist_data[base:index_to_add]]
            plot_object[i].set_data(plot_history[i][0], plot_history[i][1])
        return plot_object
    
    ani = FuncAnimation(fig, update, frames=list(range(len(Object.system[0].x_hist_data))), init_func=init, blit=True, interval=10)
    plt.show()



# MAIN
if __name__ == "__main__":
    n_bodies()