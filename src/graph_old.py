#! /usr/bin/env python3

import re

from queue import Queue, PriorityQueue

class Edge():
    def __init__(self, weight=None, flux=None, capacity=None):
        self.weight = weight
        self.flux = flux
        self.capacity = capacity

    def __str__(self):
        ",".join(["{}".format(x) for x in (self.weight,self.flux,self.capacity) if x != None])

class Vertex(dict):
    def __init__(self, key, weighted=False, value=None):
        self.key = key
        self.weighted = weighted
        self.value = value

    def connect(self, key, weight=None, flux=None, capacity=None):
        self[key] = Edge(weight=weight, flux=flux, capacity=capacity)

    def remove_connection(self, key):
        if key in self.list_connections():
            del(self[key])

    def connection_cost(self, key):
        return self[key].weight

    def list_connections(self):
        return [ key for key in self.keys() ]

    def __str__(self):
        result = [str(self.key)]
        if self.value != None:
            result.append("({0})".format(self.value))
        result.append("->")
        #def flux_and_capacity_to_string(flux, capacity):
        #    if flux != 0 or capacity != 0:
        #        return " ({0},{1})".format(flux, capacity)
        #    else:
        #        return ""
        #if not self.weighted:
        #    result.append(str(["{0}{1}".format(
        #        x, flux_and_capacity_to_string(self[x].flux, self[x].capacity)
        #    ) for x in self.list_connections()]))
        #else:
        #    result.append(str(["{0} ({1})".format(k,e.weight) for (k,e) in sorted(self.items(),
        #                                                                          key=lambda x: x[0])
        #                      ]))
        #return " ".join(result)
        result.append(str(["{0} ({1})".format(k,e) for (k,e) in sorted(self.items(),
                                                                      key=lambda x: x[0])
                         ]))
        return " ".join(result)

class Graph(dict):
    def __init__(self, weighted=False, directed=True, input_file=None):
        self.weighted = weighted
        self.directed = directed
        self.flux = False
        if input_file != None:
            self.parse_file(input_file)

    def parse_file(self, input_file):
        with open(input_file) as f:
            data = f.read().replace(" ", "").replace("\n", "").split(";")
            for entry in data:
                if entry and entry[0] == "$":
                    for sub_entry in entry[1:].split(","):
                        match = re.search(r"(.*?)\((.*?)\)", sub_entry)
                        vertex = match.group(1)
                        value = match.group(2)
                        self.create_vertex(vertex, int(value))
                elif entry and entry[0] == "#":
                    entry = entry[1:]
                    if "d" in entry:
                        self.directed = True
                    elif "u" in entry:
                        self.directed = False
                    
                    if "f" in entry:
                        self.flux = True
                    elif "w" in entry:
                        self.weighted = True
                elif entry:
                    vertices = re.search(r"(.*?)\-\>([^(]*)", entry)
                    if self.weighted:
                        value = re.search(r".*?\((.*?)\)", entry)
                    elif self.flux:
                        value = re.search(r".*?\((.*?),(.*?)\)", entry)
                    else:
                        value = None
                    start = vertices.group(1)
                    end = vertices.group(2)
                    if value != None:
                        if self.flux:
                            self.create_edge(start, end, flux=int(value.group(1)), capacity=int(value.group(2)))
                        elif self.weighted:
                            self.create_edge(start, end, weight=int(value.group(1)))
                    else:
                        self.create_edge(start, end) 

    def create_vertex(self, vertex, value=0):
        if not vertex in self.keys():
            self[vertex] = Vertex(vertex, self.weighted, value)

    def create_edge(self, s_vertex, e_vertex, weight=0, flux=0, capacity=0):
        self.create_vertex(s_vertex)
        self.create_vertex(e_vertex)
        self[s_vertex].connect(e_vertex, weight=weight, flux=flux, capacity=capacity)

    def remove_edge(self, s_vertex, e_vertex):
        self[s_vertex].remove_connection(e_vertex)

    def edge_cost(self, s_vertex, e_vertex):
        return self[s_vertex].connection_cost(e_vertex)

    def __str__(self):
        return "\n".join([ str(self[x]) for x in sorted(self.keys(), key=lambda x: x[0])])

    def _shortest_path(self, start_node, queue, distance, queue_get, queue_put):
        father = {}

        for vertex in self.keys():
            distance[vertex] = None
            father[vertex] = None

        distance[start_node] = 0
        father[start_node] = None

        queue_put(queue,start_node)

        while not queue.empty():
            node = queue_get(queue)
            for neighbour in self[node].list_connections():
                if distance[neighbour] == None or \
                     distance[node] + self.edge_cost(node, neighbour) < distance[neighbour]:
                    distance[neighbour] = distance[node] + self.edge_cost(node, neighbour)
                    father[neighbour] = node
                    queue_put(queue, neighbour)

        result = Graph()
        for vertex in self.keys():
            if father[vertex] != None:
                result.create_edge(father[vertex], vertex)
                result[vertex].value = distance[vertex]

        return result

    def dijkstra(self, start_node):
        distance = {}
        def queue_get(queue):
            return queue.get()
        def queue_put(queue, node):
            return queue.put(node)
        return self._shortest_path(start_node, Queue(), distance, queue_get, queue_put)

    def bellman(self, start_node):
        distance = {}
        def queue_get(queue):
            return queue.get()[1]
        def queue_put(queue, node):
            return queue.put((distance[node],node))
        return self._shortest_path(start_node, PriorityQueue(), distance, queue_get, queue_put)

#    def _residual_graph(self, start_

        

if __name__ == "__main__":
    g = Graph(input_file="test")
    print(g, "\n")
    res = g.bellman("1")
    print(res, "\n")
    res = g.dijkstra("1")
    print(res, "\n")
    print(g.directed)
