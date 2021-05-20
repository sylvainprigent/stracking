from ._linker import SLinkerCost


class EuclideanCost(SLinkerCost):
    """Calculate the squared euclidean distance between two objects center

    It calculated the squared distance and not the distance to save computation

    """

    def __init__(self, max_cost=1000):
        super().__init__(max_cost)

    def run(self, obj1, obj2, dt=1):
        # print('obj1=', obj1)
        # print('obj2=', obj2)
        if len(obj1) == 4:  # 3D
            return pow(obj1[1] - obj2[1], 2) + \
                   pow(obj1[2] - obj2[2], 2) + \
                   pow(obj1[3] - obj2[3], 2)
        return pow(obj1[1] - obj2[1], 2) + pow(obj1[2] - obj2[2], 2)
