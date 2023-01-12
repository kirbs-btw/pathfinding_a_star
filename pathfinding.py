import math

# algorithm name "A*"

class Node: 
    def __init__(self, pos_y = 0, pos_x = 0,):
        self.pos_y = pos_y
        self.pos_x = pos_x

class Path_node(Node):
    def __init__(self):
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
        # ---Thinking space No real comment here ---
        # could be implemented by looking at the coords of the two and if you have to change tow values to get
        # near you add 14
        # and if you just need to change one value you add 10

        # there is the easy posibility to calc it via some vector math 
        # by doing vector a minus vector b and calculating the amount (len)
        # has two down sides 
        #   - the numbers would not fit in the set sheme of a grid 
        #   - the sqrt operation is slow
        #   
        # positiv:
        # would be easy to implement xD 

        # abs() --> amount of num

        distance = 0
        """
        endNode.pos_x
        endNode.pos_y
        """

        dist_x = abs(endNode.pos_x - self.pos_x)
        dist_y = abs(endNode.pos_y - self.pos_y)
        


        
        return distance