import numpy as np
import csv
import math
import sys


class Node:
    """A node class"""

    def __init__(self, parent=None, position=None, cave_no=None):
        self.parent = parent
        self.position = position
        self.cave_no = cave_no

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


def a_star(connection, start, end, coords, size):
    # initialise start node and end node
    start_node = Node(None, start, int(coords[0, 0]))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end, [size - 1, 0])
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = set()

    open_list.append(start_node)

    # run loop whilst open list has an item
    while len(open_list) > 0:

        # set current node to first item in open list
        current_node = open_list[0]
        current_index = 0

        # compare each nodes final score in open list with current node's
        # set current node with lowest f score in open list
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # pop new current node from open list and add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node)

        # check to see if current node is end node
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(int(current.cave_no))
                current = current.parent
            return path[::-1]

        children = []
        # iterate through cave connection matrix find children of current node
        c = int(current_node.cave_no) - 1
        for r in range(size):
            if connection[r][c] == 1:
                for con in coords:
                    if r + 1 == con[0]:
                        new_node = Node(current_node, (con[1], con[2]), r + 1)
                        children.append(new_node)
                        break

        for child in children:

            # Child is in the closed list
            if child in closed_list:
                continue

            # Set f/g/h.scores if not already closed list
            child.g = current_node.g + math.sqrt((current_node.position[0] - child.position[0]) ** 2 +
                                                 (current_node.position[1] - child.position[1]) ** 2)
            child.h = math.sqrt((child.position[0] - end_node.position[0]) ** 2 +
                                (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Add child to open list if not already in
            if child not in open_list:
                open_list.append(child)

    # return path = None when there is no path
    path = None
    return path


def main():
    # get filename from command line, set file extension, remove 'caveroute' if included in the input
    filename = sys.argv[1]
    filename += ".cav"
    if "caveroute" in filename:
        filename = filename.replace('caveroute ', '')

    # read the selected file, remove ',' and prepare new file with .csn
    with open(filename) as cav_file:
        cav_file = csv.reader(cav_file, delimiter=',')
        file2 = filename.replace('.cav', '.csn')

        for line in cav_file:
            # initialising variables and arrays
            i = 0
            size = int(line[i])
            coord_list = np.zeros(shape=(size, 3))
            connections = np.zeros(shape=(size, size))

            # populating coord list
            for r in range(size):
                i += 2
                for c in range(3):
                    if c == 0:
                        coord_list[r][c] = r + 1
                    elif c == 1:
                        coord_list[r][c] = line[i - 1]
                    elif c == 2:
                        coord_list[r][c] = line[i]

            # populating connection matrix
            new_size = size * 2 + 1
            for c in range(size):
                for r in range(size):
                    if int(line[new_size]) == 1:
                        connections[c][r] = line[new_size]
                    new_size += 1

        start = (coord_list[0, 1], coord_list[0, 2])
        end = (coord_list[size - 1, 1], coord_list[size - 1, 2])

        # return path from start to end node
        path = a_star(connections, start, end, coord_list, size)

        # create filename.csn files containing the path robot took
        if path is None:
            print(0, file=open(file2, 'w'))
        else:
            print(*path, file=open(file2, 'w'))


if __name__ == '__main__':
    main()
