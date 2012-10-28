from node import *

## @class LinkedList
#  @brief this class contains a linked list of nodes
class LinkedList(object):
    def __init__(self):
        #reference to first node
        self.first = None
        #reference to last node
        self.last = None
        #number of nodes in list
        self.size = 0

    ## the append function
    #  @brief takes in a node and adds it to the end of the list
    def append(self, new_node):
        #are we empty?
        if(self.size == 0):
            self.first = self.last = new_node

        #add node to the end
        self.last.next_node = new_node

        #update prev
        new_node.prev_node = self.last

        #update next
        new_node.next_node = None

        #update reference to last element
        self.last = new_node

        #update size
        self.size += 1

    ## the insert function
    #  @brief a wrapper for insert_right
    def insert(self, old_node, new_node):
        insert_right(old_node, new_node)

    ## the insert_right function
    #  @brief inserts a node to the right of the given node
    def insert_right(self, old_node, new_node):
        #update reference to last node if needed
        if(old_node.next_node == None):
            self.last = new_node
        #not the end of list, so make sure next's prev is updated
        else:
            old_node.next_node.prev_node = new_node
        
        #update reference to next
        new_node.next_node = old_node.next_node

        #update reference to prev
        new_node.prev_node = old_node

        #update old's next
        old_node.next_node = new_node

        #update size
        self.size += 1

    ## the insert_left function
    #  @brief inserts a node to the left of the given node
    def insert_left(self, old_node, new_node):
        #update reference to first node if needed
        if(old_node.prev_node == None):
            self.first = new_node
        #not at the start of list, update prev's next
        else:
            old_node.prev_node.next_node = new_node

        #update reference to next
        new_node.next_node = old_node

        #update reference to prev
        new_node.prev_node = old_node.prev

        #update old's prev
        old_node.prev_node = new_node

        #update size
        self.size += 1

    ## the delete function
    #  @brief removes the given node from the list
    def delete(self, dead_node):
        #update prev's next
        if(dead_node.prev_node != None):
            dead_node.prev_node.next_node = dead_node.next_node
        #its at the start, update first reference
        else:
            self.first = dead_node.next_node

        #update next's prev
        if(dead_node.next_node != None):
          dead_node.next_node.prev_node = dead_node.prev_node
        #its at the end, update last reference
        else:
            self.last = dead_node.prev_node

        self.size -= 1

    ## the __iter__ function
    #  @brief returns an iterator to the list, so we can be iterable
    def __iter__(self):
        return self.first
