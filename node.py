## @class Node
#  @brief this class is a node in the LinkedList class
class Node(object):
    ## the constructor
    #  @brief sets the references
    def __init__(self):
        self.next_node = None
        self.prev_node = None

    ## the __iter__ furnction
    #  @brief returns an interator (ourself)
    def __iter__(self):
        return self

    ## the next function
    #  @brief because we're an iterator too!
    def next(self):
        if self.next_node == None:
            raise StopIteration
        else:
            return self.next_node
