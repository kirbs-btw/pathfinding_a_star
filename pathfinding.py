# algorithm name "A*"

class Node: 
    def __init__(self, pos_y = 0, pos_x = 0,):
        self.pos_y = pos_y
        self.pos_x = pos_x

class Path_node(Node):
    def __init__(self, g_cost = 0):
        self.g_cost = g_cost
        # distance to start node according to the path
        # can be calc by adding the prev g_cost of the node it came from + the cost to produce

        self.h_cost = self.get_h_cost()
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

# Bastian Lipka