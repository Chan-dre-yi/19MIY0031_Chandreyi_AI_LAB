
    
# coding=utf-8
"""
This file is your main submission that will be graded against. Only copy-paste
code on the relevant classes included here. Do not add any classes or functions
to this file that are not part of the classes that we want.
"""

import heapq
import sys
import math


from util import generate_graph

max_possible_value = sys.maxsize


class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority.

    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.

    Traditionally priority queues are implemented with heaps, but there are any
    number of implementation options.

    (Hint: take a look at the module heapq)

    Attributes:
        queue (list): Nodes added to the priority queue.
    """

    def _init_(self):
        """Initialize a new Priority Queue."""

        self.queue = []

    def pop(self):
        """
        Pop top priority node from queue.

        Returns:
            The node with the highest priority.
        """
        return heapq.heappop(self.queue)

    def remove(self, node_id):
        """
        Remove a node from the queue.

        This is a hint, you might require this in ucs,
        however, if you choose not to use it, you are free to
        define your own method and not use it.

        Args:
            node_id (int): Index of node in queue.
        """
        self.queue.pop(node_id)
        heapq.heapify(self.queue)

    def _iter_(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def _str_(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node: Comparable Object to be added to the priority queue.
        """
        heapq.heappush(self.queue, node)

    def _contains_(self, key):
        """
        Containment Check operator for 'in'

        Args:
            key: The key to check for in the queue.

        Returns:
            True if key is found in queue, False otherwise.
        """

        return key in [n for _, n in self.queue]

    def _eq_(self, other):
        """
        Compare this Priority Queue with another Priority Queue.

        Args:
            other (PriorityQueue): Priority Queue to compare against.

        Returns:
            True if the two priority queues are equivalent.
        """

        return self.queue == other.queue

    def size(self):
        """
        Get the current size of the queue.

        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue = []

    def top(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in teh queue.
        """

        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return 0, None


def uniform_cost_search(graph, start, goal):
    path = []
    explored_nodes = list()

    if start == goal:
        return path, explored_nodes

    path.append(start)
    path_cost = 0

    frontier = [(path_cost, path)]
    while len(frontier) > 0:
        # pop a node from the queue
        path_cost_till_now, path_till_now = pop_frontier(frontier)
        current_node = path_till_now[-1]
        explored_nodes.append(current_node)

        # test goal condition
        if current_node == goal:
            return path_till_now, explored_nodes

        neighbours = graph[current_node]

        neighbours_list_int = [int(n) for n in neighbours]
        neighbours_list_int.sort(reverse=False)
        neighbours_list_str = [str(n) for n in neighbours_list_int]

        for neighbour in neighbours_list_str:
            path_to_neighbour = path_till_now.copy()
            path_to_neighbour.append(neighbour)

            extra_cost = 1
            neighbour_cost = extra_cost 
            """+ path_cost_till_now"""
            new_element = (neighbour_cost, path_to_neighbour)

            is_there, indexx, neighbour_old_cost, _ = get_frontier_params_new(neighbour, frontier)

            if (neighbour not in explored_nodes) and not is_there:
                frontier.append(new_element)
            # If the neighbour is in frontier but there exists a
            # costlier path to this neighbour, remove that costly path
            elif is_there:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(indexx)
                    frontier.append(new_element)

    return None, None


def is_this_node_in_frontier(node, frontier):
    for path in frontier:
        if node == path[-1]:
            return True
    return False


def greedy_search(graph, start, goal):

    path = []
    explored_nodes = list()

    # Edge case check
    if start == goal:
        return path, explored_nodes

    path.append(start)
    path_cost = get_geographical_heuristic(start, goal)
    # Priority Queue to keep sorted distance travelled till now
    frontier = [(path_cost, path)]
    while len(frontier) > 0:
        # pop a node from the queue
        path_cost_till_now, path_till_now = pop_frontier(frontier)
        current_node = path_till_now[-1]
        #path_cost_till_now = path_cost_till_now - get_geographical_heuristic(current_node, goal)
        explored_nodes.append(current_node)
        # test goal condition
        if current_node == goal:
            return path_till_now, explored_nodes

        neighbours = graph[current_node]

        neighbours_list_int = [int(n) for n in neighbours]
        neighbours_list_int.sort(reverse=False)
        neighbours_list_str = [str(n) for n in neighbours_list_int]

        for neighbour in neighbours_list_str:
            path_to_neighbour = path_till_now.copy()
            path_to_neighbour.append(neighbour)

            # extra_cost = graph.get_edge_weight(current_node, neighbour)
            extra_cost = 1
            neighbour_cost = extra_cost + get_geographical_heuristic(neighbour, goal)
            """+ path_cost_till_now""" 
            new_element = (neighbour_cost, path_to_neighbour)

            is_there, indexx, neighbour_old_cost, _ = get_frontier_params_new(neighbour, frontier)

            if (neighbour not in explored_nodes) and not is_there:
                frontier.append(new_element)

            # If the neighbour is in frontier but there exists a
            # costlier path to this neighbour, remove that costly path
            elif is_there:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(indexx)
                    frontier.append(new_element)

    return None, None


def pop_frontier(frontier):
    if len(frontier) == 0:
        return None
    # copied_list = frontier.copy()
    min = max_possible_value
    max_values = []
    for key, path in frontier:
        if key == min:
            max_values.append(path)
        elif key < min:
            min = key
            max_values.clear()
            max_values.append(path)

    max_values = sorted(max_values, key=lambda x: x[-1])
    # max_values.sort()
    desired_value = max_values[0]
    frontier.remove((min, max_values[0]))
    return min, desired_value


def get_frontier_params_new(node, frontier):
    for i in range(len(frontier)):
        curr_tuple = frontier[i]
        cost, path = curr_tuple
        if path[-1] == node:
            return True, i, cost, path

    return False, None, None, None


def get_frontier_params(node, frontier):
    for i in range(len(frontier.queue)):
        curr_tuple = frontier.queue[i]
        cost, path = curr_tuple
        if path[-1] == node:
            return True, i, cost, path

    return False, None, None, None


def get_geographical_heuristic(node, goal):
    i, j = divmod(int(node), 8)
    i_goal, j_goal = divmod(int(goal), 8)
    i_delta = (i - i_goal)**2
    j_delta = (j - j_goal)**2

    geographical_dist = math.sqrt(i_delta + j_delta)
    return geographical_dist


if __name__ == '__main__':
    graph_neighbours = generate_graph()

    print("============ UCS Search ================")
    path_ucs, explored_ucs = uniform_cost_search(graph_neighbours, '0', '3')
    print("Path UCS:", path_ucs)
    # print("Explored Nodes UCS: ", explored_ucs)
    print(len(explored_ucs))
    print()

    print("============ Greedy Search ================")
    path_astar, explored_astar = greedy_search(graph_neighbours, '0', '3')
    print("Path_greedy:", path_astar)
    print("Explored Nodes Greedy: ", explored_astar)
    print(len(explored_astar))
    print()

   
