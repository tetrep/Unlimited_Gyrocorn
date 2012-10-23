from node import *

## @class LinkedList
#  @brief this class contains a linked list of nodes
class LinkedList(object):
    def __init__(self):
        #reference to first node
        this.first = None
        #reference to last node
        this.last = None
        #number of nodes in list
        this.size = 0

    ## the append function
    #  @brief takes in a node and adds it to the end of the list
    def append(self, new_node):
        if(this.size == 0):
            this.first = this.last = new_node
        else:
            #add node to the end
            this.last.next_node = new_node

            #update prev
            new_node.prev_node = this.last

            #update next
            new_node.next_node = None

            #update reference to last element
            this.last = new_node

            #update size
            this.size++

    ## the insert function
    #  @brief a wrapper for insert_right
    def insert(self, old_node, new_node):
        insert_right(old_node, new_node)

    ## the insert_right function
    #  @brief inserts a node to the right of the given node
    def insert_right(self, old_node, new_node):
        #update reference to last node if needed
        if(old_node.next_node == None):
            this.last = new_node
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
        this.size++

    ## the insert_left function
    #  @brief inserts a node to the left of the given node
    def insert_left(self, old_node, new_node):
        #update reference to first node if needed
        if(old_node.prev_node == None):
            this.first = new_node
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
        this.size++

    ## the delete function
    #  @brief removes the given node from the list
    def delete(self, dead_node):
        #update prev's next
        if(dead_node.prev_node != None):
            dead_node.prev_node.next_node = dead_node.next_node
        #its at the start, update first reference
        else:
            this.first = dead_node.next_node

        #update next's prev
        if(dead_node.next_node != None):
          dead_node.next_node.prev_node = dead_node.prev_node
        #its at the end, update last reference
        else:
            this.last = dead_node.prev_node

        this.size--
