#! /usr/bin/env python3

import re

from queue import Queue, PriorityQueue

class Edge():
    """Graph edge

    This class represents an edge in a graph

    Attributes:
    start:      The node the edge starts from
    end:        The node the edge ends into
    weight:     The value of the weight of the edge
    capacity:   The amount of flux the edge can carry
    lbound:     The amount of flux the edge has to carry, at least
    flux:       The amount of flux currently passing through the edge

    Invariant:
    end != None and
    capacity == None or capacity >= 0 and
        lbound == None or 0 <= lbound and
    (capacity != None and lbound != None -> lbound <= capacity)
    """

    def __init__(self, end, start=None, weight=None,
                 capacity=None, lbound=None, flux=None):
        """Class constructor

        Args:
            end:        The node the edge ends into
            start:      The node the edge starts from; None if not declared
            weight:     The value of the weight of the edge; None if not declared
            capacity:   The amount of flux the edge can carry; None if not declared
                        (must be None or not lesser than 0)
            lbound:     The amount of flux the edge has to carry, at least; None if
                        not declared (must be None or not lesser than 0 and not
                        greater than capacity)
            flux:       The amount of flux currently passing through the edge; None
                        if not declared

            Raises:
                ValueError: Raised if some restrictions on the arguments were
                            violated
        """ 
        if capacity != None and capacity < 0:
            raise ValueError("Negative capacity")
        if lbound != None:
            if lbound < 0:
                raise ValueError("Negative lbound")
            elif capacity != None and lbound > capacity:
                raise ValueError("Incompatible lbound and capacity")
        
        self.start = start
        self.end = end
        self.weight = weight
        self.capacity = capacity
        self.lbound = lbound
        self.flux = flux


    def rep_ok(self):
        """Class invariant check"""
        assert self.end != None, "end invariant violated in Edge class"
        assert self.capacity == None or self.capacity >= 0,\
                "capacity invariant violated in Edge class"
        assert self.lbound == None or self.lbound >= 0,\
                "lbound invariant violated in Edge class"
        if (self.capacity != None and self.lbound != None):
            assert self.lbound <= self.capacity,\
                "lbound <= capacity invariant violated in Edge class"

    def __str__(self):
        if self.start != None:
            start_end = "{} -> {}".format(self.start, self.end)
        else:
            start_end = "{}".format(self.end)
        metadata = []
        if self.weight != None:
            metadata.append("$" + str(self.weight))
        if self.lbound != None:
            metadata.append("m" + str(self.lbound))
        if self.capacity != None:
            metadata.append("M" + str(self.capacity))
        if self.flux != None:
            metadata.append("~" + str(self.flux))
        
        if metadata:
            metadata = ";".join(metadata)
            metadata = "(" + metadata + ") "
        else:
            metadata = ""

        return "{}{}".format(metadata, start_end)

class Vertex(dict):
    """Graph vertex

    A graph vertex is a dictionary-like class; if vertex_start is connected to
    node of label vertex_end, vertex_start[vertex_end] is the edge which details
    the connection

    Attributes:
        label:  The name of the node.
        value:  The value of the node; usually, the quantity of goods it must
                produce / receive
    """

    def __init__(self, label, value=None):
        """Class constructor

        Args:
            label:  Attribute.
            value:  Attribute. None if not declared
        """
        super().__init__()
        self.label = label
        self.value = value

    def connect(self, end, weight=None, capacity=None, lbound=None, flux=None):
        """Connects the vertex to another

        Args:
            end:        The label of the vertex to be connected
            weight:     The weight of the edge
            capacity:   The capacity of the edge
            lbound:     The lbound of the edge
            flux:       The flux of the edge
        """
        self[end] = Edge(end=end, weight=weight,
                         capacity=capacity, lbound=lbound, flux=flux)

    def list_connected_nodes(self):
        """Returns a list of connected nodes

        Returns a list made of the labels of the connected nodes

        Returns:
            A list of the labels of the connected nodes, sorted
        """
        return sorted(self)

    def is_connected(self, end):
        """Check if the vertex is connected to the given one

        Args:
            end:    The label of the vertex with which the connection is checked
        Returns:
            True if the vertex is connected to end, False otherwise
        """
        return (end in self)

    def get_weight(self, end):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        return self[end].weight

    def get_capacity(self, end):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        return self[end].capacity

    def get_lbound(self, end):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        return self[end].lbound

    def get_flux(self, end):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        return self[end].flux

    def set_weight(self, end, value):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        self[end].weight = value

    def set_capacity(self, end, value):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        self[end].capacity = value

    def set_lbound(self, end, value):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        self[end].lbound = value

    def set_flux(self, end, value):
        if not self.is_connected(end):
            raise KeyError("Vertex not connected")
        self[end].flux = value 

    def __str__(self):
        return "{} -> [{}]".format(
            self.label,
            ", ".join([str(self[x]) for x in self]))

    def __lt__(self,other):
        return self.label < other.label
    def __gt__(self,other):
        return self.label > other.label
    def __le__(self,other):
        return self.label <= other.label
    def __ge__(self,other):
        return self.label >= other.label

    def __hash__(self):
        return self.label.__hash__()

    def __iter__(self):
        for val in sorted(self.keys()):
            yield val 

class Graph():
    """A graph is a set of vertexes connected between them

    Attributes:
        directed:   A boolean; True if and only if the graph is directed
        vertexes:   A mapping of labels to vertexes; if the node of label
                    v is in the graph, self[v] is the vertex
    String:
        The graph represented by adjacency lists
    Iterator:
        A sorted list of the labels of the vertexes 
    """

    def __init__(self, directed=True):
        """Class constructor

        Args:
            directed:   Attribute.
        Raises:
            ValueError: directed wasn't boolean
        """
        if directed != False and directed != True:
            raise ValueError("Boolean not false and not true")
        self.directed = directed
        self.vertexes = dict()

    def add_vertex(self, vertex, value=None):
        """Adds the given vertex to the graph

        Args:
            vertex: An instance of Vertex, or an hashable label
            value:  To be set only if vertex isn't of Vertex class,
                    used as the value of the vertex
        """
        if isinstance(vertex, Vertex):
            self.vertexes[vertex.label] = vertex
        else:
            self.vertexes[vertex] = Vertex(vertex,value)

    def is_vertex_in(self, vertex):
        """Checks if a vertex is in the graph

        Args:
            vertex: An instance of Vertex, or an hashable label.
                    The check is in any case based on the label
                    of the vertex
        """
        if isinstance(vertex, Vertex):
            label = vertex.label
        else:
            label = vertex
        return (label in self.vertexes)

    def add_edge(self, start_vertex, end_vertex, weight=None,
                 capacity=None, lbound=None, flux=None):
        """Creates a connection between start_vartex and end_vertex

        Args:
            start_vertex:   The vertex from which the connection starts
            end_vertex:     The vertex at which the connection ends
            weight:         Weight of the edge
            capacity:       Capacity of the edge
            lbound:         Lower bound of the edge
            flux:           Flux through the edge
        """
        if isinstance(start_vertex, Vertex):
            start_label=start_vertex.label
            start_value=start_vertex.value
        else:
            start_label=start_vertex
            start_value=None
        if not self.is_vertex_in(start_label):
            self.add_vertex(start_label,start_value)
        if isinstance(end_vertex, Vertex):
            end_label=end_vertex.label
            end_value=end_vertex.value
        else:
            end_label=end_vertex
            end_value=None
        if not self.is_vertex_in(end_label):
            self.add_vertex(end_label,end_value)
        self.vertexes[start_label].connect(end=end_label,weight=weight,
                                           capacity=capacity, lbound=lbound,
                                           flux=flux)
    def iterate_connections(self,start_label):
        """Returns an iterator of FS of start_label
            
        Args:
            start_label The label of the starting node
        """
        for v in self.vertexes[start_label]:
            yield v

    def __str__(self):
        return "\n".join([str(self.vertexes[l]) for l in sorted(self.vertexes)])

    def __iter__(self):
        for val in sorted(self.vertexes.keys()):
            yield val 

if __name__ == "__main__":
    e = Edge(end=4, weight=12, capacity=50, lbound=3, flux=10)
    print(e)
    print(Edge(end=3, weight=5))

    v = Vertex(2)
    v.connect(end=4, weight=5)
    v.connect(end=5, weight=6)
    print(v)
    print()

    g = Graph()
    g.add_edge(5,6,weight=5)
    g.add_edge(5,7,weight=7)
    g.add_edge(6,7,weight=12)
    print(g)
    print(g.iterate_connections(5))
    for v in g.iterate_connections(5):
        print(v)
