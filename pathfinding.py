# algorithm name "A*"

class Grid: 
    def __init__(self, size):
        self.grid = self.initGrid(size)

    def initGrid(self, size) -> list:

        grid = []

        for i in range(size):
            row = []
            for j in range(size):
                row.append([j, i])        # append a path_node with the correct coords  
            grid.append(row)
        return grid

    def print(self) -> None:
        for row in self.grid:
            print(row)

    def __str__(self) -> None:
        return "Size: {}, Items: {}".format(len(self.grid), len(self.grid)**2)

class Obstacle:
    def __init__(self):
        pass

class Node: 
    def __init__(self, pos_y : int, pos_x : int,):
        self.pos_y = pos_y
        self.pos_x = pos_x


class Path_node(Node):
    def __init__(self, endNode : Node, g_cost = None):
        self.g_cost = g_cost # ist none when started 
        # distance to start node according to the path
        # can be calc by adding the prev g_cost of the node it came from + the cost to produce

        self.h_cost = self.get_h_cost(endNode)
        # distance to end node in the fastest way without obstacle
        # could be calculated with the pos of the end node and the own pos

        self.f_cost = self.g_cost + self.h_cost
        # a value to indicate the worth 
        # combines g_cost with h_cost
    
    def get_h_cost(self, endNode : Node) -> int:
        """
        calculates the distance of the node to the end node
        without the obstacles
        """

        dist_a = abs(endNode.pos_x - self.pos_x)
        dist_b = abs(endNode.pos_y - self.pos_y)
        
        if dist_a < dist_b:
            dist_a, dist_b = dist_b, dist_a

        distance = dist_b * 14 + (dist_a - dist_b) * 10
        
        return distance

    def __str__(self) -> None:
        return f"Pos: [{self.pos_x}, {self.pos_y}], g_cost = {self.g_cost}, h_cost = {self.h_cost}, f_cost = {self.f_cost}"

if __name__ == '__main__':
    field = Grid(5)
    print(field)



# Bastian Lipka