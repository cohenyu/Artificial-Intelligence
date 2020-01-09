
def ordered_set(coll):
    return dict.fromkeys(coll).keys()


class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def neighbors(self, roads, f):
        return [Node(link.target, self, self.path_cost + f(link)) for link in roads[self.state].links]
        # neighbors_list = []
        # for link in roads[self.state].links:
        #     neighbors_list.append(Node(link.target, self, self.path_cost + f(link)))
        # return neighbors_list

    def solution(self):
        return [node.state for node in self.path()]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.state)
