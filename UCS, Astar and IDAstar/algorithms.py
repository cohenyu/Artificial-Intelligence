from ways import info
from ways import load_map_from_csv
from node import Node
from priority_queue import PriorityQueue
from ways import tools
import math
# import csv
# import matplotlib.pyplot as plt
# import timeit
# import numpy as np
# from ways import draw


roads = load_map_from_csv()


# this function starts the ucs algorithm and defined the g() function
def ucs(src, goal):
    def g(link):
        return link.distance / max(info.SPEED_RANGES[link.highway_type]) / 1000
    return best_first_graph_search(src, goal, f=g)


# this function starts the astar and idastar algorithms according the mode param
def a_star(src, goal, mode):
    # definition of g(), h(), g()+h() functions
    def g(link):
        return link.distance / max(info.SPEED_RANGES[link.highway_type]) / 1000

    def h(link):
        source = roads[link.target]
        target = roads[goal]

        if link.source == src:
            prev = 0
        else:
            parent = roads[link.source]
            prev = tools.compute_distance(parent.lat,parent.lon, target.lat, target.lon) / 110

        return (tools.compute_distance(source.lat, source.lon, target.lat, target.lon) / 110) - prev

    def cost(link):
        return g(link) + h(link)

    if mode == 'a':
        return best_first_graph_search(src, goal, cost)
    elif mode == 'ida':
        return iterative_deepening_search(src, goal, cost)


# This is the depth limited search algorithm
def depth_limited_search(node, goal, f, f_limit):
    if node.path_cost > f_limit:
        return None, node.path_cost, None
    # if it is the goal node - done
    if node.state == goal:
        return node.solution(), f_limit, node.path_cost
    new_limit = math.inf
    # loop over his neighbors
    for n in node.neighbors(roads, f):
        solution, new_f, cost = depth_limited_search(n, goal, f, f_limit)
        if solution:
            return solution, f_limit, cost
        new_limit = min(new_limit, new_f)
    return None, new_limit, None


# This is the iterative deepening search algorithm
def iterative_deepening_search(start, goal, f):
    source = roads[start]
    target = roads[goal]
    # calculate the first heuristic function
    f_limit = (tools.compute_distance(source.lat, source.lon, target.lat, target.lon) / 110)
    start_node = Node(start)
    # search the solution
    while True:
        result, f_limit, cost = depth_limited_search(start_node, goal, f, f_limit)
        if result:
            return result


# This is the best first graph search algorithm
def best_first_graph_search(start, goal, f):
    node = Node(start)
    open_list = PriorityQueue(lambda x: x.path_cost)
    # insert the first node to the open list
    open_list.append(node)
    closed_list = set()
    # As long as there is an node in the open list:
    while open_list:
        # pop the first node from the priority queue
        node = open_list.pop()
        # if it is the goal node - done
        if node.state == goal:
            return node.solution()
        # if not - put it in the list of nodes we've already visited.
        closed_list.add(node.state)
        # loop over his neighbors
        for neighbor in node.neighbors(roads, f):
            if neighbor.state not in closed_list and neighbor not in open_list:
                # insert the node to the open list
                open_list.append(neighbor)
            elif neighbor in open_list and neighbor.path_cost < open_list[neighbor]:
                # switch between them
                del open_list[neighbor]
                open_list.append(neighbor)
    return None


# def ucs_results():
#     times = []
#     file = open('results/UCSRuns.txt', 'w')
#     with open('db/problems.csv') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for line in csv_reader:
#             src = int(line[0])
#             goal = int(line[1])
#             start = timeit.default_timer()
#             result, path_cost = ucs(src, goal)
#             end = timeit.default_timer()
#             print(result)
#             times.append(end - start)
#             file.write(str(path_cost) + '\n')
#     file.close()
#     avg = np.mean(times)
#     std = np.std(times)
#     print('UCS: avg =', avg, 'std =', std)
#
#
# def astar_results():
#     times = []
#     file = open('results/AStarRuns.txt', 'w')
#     heuristic = []
#     actual = []
#     with open('db/problems.csv') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for idx, line in enumerate(csv_reader):
#             src = int(line[0])
#             goal = int(line[1])
#             start = timeit.default_timer()
#             result, path_cost = a_star(src, goal, 'a')
#             end = timeit.default_timer()
#             print(result)
#             times.append(end - start)
#             u = tools.compute_distance(roads[src].lat, roads[src].lon, roads[goal].lat, roads[goal].lon) / 110
#             file.write(str(u) + ' ' + str(path_cost) + '\n')
#             heuristic.append(u)
#             actual.append(path_cost)
#             if idx < 10:
#                 draw.plot_path(roads, result)
#                 plt.show()
#     avg = np.mean(times)
#     std = np.std(times)
#     print('AStar: avg =', avg, 'std =', std)
#     csv_file.close()
#     file.close()
#     # plt.xlabel('Time estimated by heuristics')
#     # plt.ylabel('Actual travel time')
#     # plt.plot(heuristic, actual, 'ro')
#     # plt.show()
#
#
# def idastar_results():
#     times = []
#     heuristic = []
#     actual = []
#     file = open('results/IDAStarRuns.txt', 'w')
#     with open('db/problems.csv') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for idx, line in enumerate(csv_reader):
#             src = int(line[0])
#             goal = int(line[1])
#             start = timeit.default_timer()
#             result, path_cost = a_star(src, goal, 'ida')
#             end = timeit.default_timer()
#             print(result)
#             times.append(end - start)
#             u = tools.compute_distance(roads[src].lat, roads[src].lon, roads[goal].lat, roads[goal].lon) / 110
#             file.write(str(u) + ' ' + str(path_cost) + '\n')
#             heuristic.append(u)
#             actual.append(path_cost)
#             if idx == 4:
#                 break
#     csv_file.close()
#     file.close()
#     plt.xlabel('Time estimated by heuristics')
#     plt.ylabel('Actual travel time')
#     plt.plot(heuristic, actual, 'ro')
#     plt.show()
#     avg = np.mean(times)
#     std = np.std(times)
#     print('IDAStar: avg =', avg, 'std =', std)


# if __name__ == '__main__':
#     idastar_results()
#     astar_results()
#     ucs_results()

