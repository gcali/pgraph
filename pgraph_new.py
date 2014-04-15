#! /usr/bin/env python3

from collections import Hashable
from types import GeneratorType
import itertools

class Edge():
    """Edge class
    """

    def __init__(self, end_label:object, weight:int, lbound:int,
                       ubound:int, flux:int) -> None:
        """constructor
        """
        self.end_label = end_label
        self.weight = weight
        self.lbound = lbound
        self.ubound = ubound
        self.flux = flux

    def get_weight(self:Hashable) -> int:
        """Returns the current weight 
        """
        return self.weight

    def set_weight(self, weight) -> None:
        """Sets the current weight 
        """
        self.weight = weight

    def get_lbound(self) -> int:
        """Returns the current lbound 
        """
        return self.lbound

    def set_lbound(self, lbound) -> None:
        """Sets the current lbound 
        """
        self.lbound = lbound

    def get_ubound(self) -> int:
        """Returns the current ubound 
        """
        return self.ubound

    def set_ubound(self, ubound) -> None:
        """Sets the current ubound 
        """
        self.ubound = ubound

    def get_flux(self) -> int:
        """Returns the current flux 
        """
        return self.flux

    def set_flux(self, flux) -> None:
        """Sets the current flux 
        """
        self.flux = flux

    def __str__(self):
        metadata = []
        if self.weight != None:
            metadata.append("$" + str(self.weight))
        if self.lbound != None:
            metadata.append("b" + str(self.lbound))
        if self.ubound != None:
            metadata.append("B" + str(self.ubound))
        if self.flux != None:
            metadata.append("~" + str(self.flux))

        metadata = ";".join(metadata)
        if metadata:
            metadata = "(" + metadata + ")"

        return "{}{}".format(metadata, str(self.end_label))


class Node():
    """Node class
    """

    def __init__(self, label:object, value:int) -> None:
        """constructor
        """
        self.label = label
        self.value = value
        self.connections = {}

    def connect(self, end_label:Hashable, weight:int, lbound:int,
                      ubound:int, flux:int) -> None:
        """Connect the node to another one"""
        self.connections[end_label] = Edge(end_label, weight, lbound,
                                           ubound, flux)

    def remove_connection(self, end_label:Hashable) -> None:
        """Remove a connection

        Raises:
            KeyError:   end_label wasn't found in the graph
        """
        del(self.connections[end_label])

    def is_connected(self, end_label:Hashable) -> bool:
        """Returns True iff the node is connected to end_label
        """
        return end_label in self.connections

    def forward_star(self) -> GeneratorType:
        """Returns an iterator of the forward star of the current node
        """
        for node in self.connections:
            yield node

    def get_value(self) -> int:
        """Returns the current value of the node
        """
        return self.value

    def set_value(self, value:int) -> None:
        """Sets the current value of the node
        """
        self.value = value

    def get_weight(self, end_label:Hashable) -> int:
        """Returns the current weight to end_label

        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        return self.connections[end_label].get_weight()

    def set_weight(self, end_label, weight) -> None:
        """Sets the current weight to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        self.connections[end_label].set_weight(weight)

    def get_lbound(self, end_label) -> int:
        """Returns the current lbound to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        return self.connections[end_label].get_lbound()

    def set_lbound(self, end_label, lbound) -> None:
        """Sets the current lbound to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        self.connections[end_label].set_lbound(lbound)

    def get_ubound(self, end_label) -> int:
        """Returns the current ubound to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        return self.connections[end_label].get_ubound()

    def set_ubound(self, end_label, ubound) -> None:
        """Sets the current ubound to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        self.connections[end_label].set_ubound(ubound)

    def get_flux(self, end_label) -> int:
        """Returns the current flux to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        return self.connections[end_label].get_flux()

    def set_flux(self, end_label, flux) -> None:
        """Sets the current flux to end_label
        
        Raises:
            KeyError:   end_label wasn't found
                        in the connections
        """
        self.connections[end_label].set_flux(flux)

    def __str__(self):
        def comparison_function(edge):
            return edge.end_label
        return "{} -> {}".format(
            str(self.label),
            ", ".join((str(x) for x in
                       sorted(self.connections.values(),
                       key=comparison_function)))
            )

class Graph():
    """Graph class
    """

    def __init__(self, directed=True) -> None:
        """constructor
        """
        self.node_map = {}
        self.directed = directed

    def add_node(self, label:Hashable, value:int=None) -> None:
        """Adds a node to the graph
        """
        if label not in self.list_nodes():
            self.node_map[label] = Node(label, value)

    def add_connection(self, start_label:Hashable, end_label:Hashable,
                             weight:int=None, lbound:int=None,
                             ubound:int=None, flux:int=None) -> None:
        """Adds a connection to the graph
        """
        self.add_node(start_label)
        self.add_node(end_label)
        if self.directed or start_label <= end_label:
            self.node_map[start_label].connect(end_label, weight, lbound,
                                               ubound, flux)
        else:
            self.node_map[end_label].connect(start_label, weight, lbound,
                                             ubound, flux)
    
    def remove_connection(self, start_label:Hashable,
                          end_label:Hashable) -> None:
        """Remove a connection from the graph

        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        self.node_map[start_label].remove_connection(end_label)

    def is_connected(self, start_label:Hashable, end_label:Hashable) -> bool:
        """Returns True iff start_label -> end_label
        """
        try:
            return self.node_map[start_label].is_connected(end_label)
        except KeyError:
            return False

    def list_nodes(self) -> GeneratorType:
        """Returns an iterator of the nodes currently in the graph
        """
        for node in sorted(self.node_map.keys()):
            yield node

    def forward_star(self, start_label:Hashable) -> GeneratorType:
        """Returns an iterator of the nodes reachable from start_label

        Raises:
            KeyError:   start_label wasn't found in the graph
        """
        if self.directed:
            return self.node_map[start_label].forward_star()
        else:
            return itertools.chain(self.node_map[start_label].forward_star(),
                                   self.backward_star(start_label))
            
    
    def backward_star(self, end_label:Hashable) -> GeneratorType:
        """Returns an iterator of the nodes from which end_label can be reached

        Raises:
            KeyError:   start_label wasn't found in the graph
        """
        for node in self.list_nodes():
            if self.is_connected(node, end_label):
                yield node 

    def get_node_value(self, label:Hashable) -> int:
        """Returns the value of the node label
        
        Raises:
            KeyError:   label wasn't found in the graph
        """
        return self[label].get_value()

    def set_node_value(self, label:Hashable, value:int) -> None:
        """Sets the value of the node label

        Raises:
            KeyError:   label wasn't found in the graph
        """
        self[label].set_value(value)

    def get_weight(self, start_label:Hashable, end_label:Hashable) -> int:
        """Returns the current weight from start_label to end_label

        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        return self.node_map[start_label].get_weight(end_label)

    def set_weight(self, start_label:Hashable, end_label, weight) -> None:
        """Sets the current weight from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        self.node_map[start_label].set_weight(end_label, weight)

    def get_lbound(self, start_label, end_label) -> int:
        """Returns the current lbound from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        return self.node_map[start_label].get_lbound(end_label)

    def set_lbound(self, start_label, end_label, lbound) -> None:
        """Sets the current lbound from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        self.node_map[start_label].set_lbound(end_label, lbound)

    def get_ubound(self, start_label, end_label) -> int:
        """Returns the current ubound from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        return self.node_map[start_label].get_ubound(end_label)

    def set_ubound(self, start_label, end_label, ubound) -> None:
        """Sets the current ubound from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        self.node_map[start_label].set_ubound(end_label, ubound)

    def get_flux(self, start_label, end_label) -> int:
        """Returns the current flux from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        return self.node_map[start_label].get_flux(end_label)

    def set_flux(self, start_label, end_label, flux) -> None:
        """Sets the current flux from start_label to end_label
        
        Raises:
            KeyError:   either start_label or end_label weren't found
                        in the graph
        """
        self.node_map[start_label].set_flux(end_label, flux)

    def __str__(self):
        graph_list = []
        for node in self.list_nodes():
            graph_list.append(str(self.node_map[node]))
        return "\n".join(graph_list)

            

if __name__ == '__main__':
    g = Graph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_connection(1,2)
    g.add_connection(1,3, weight=3, ubound=15, flux=12)
    g.add_connection(2,3)
    g.add_connection(3,4)
    g.add_connection(4,1)
    print(g)
    print("Forward star 1")
    for n in g.forward_star(1):
        print(n)
    print("Forward star 4")
    for n in g.forward_star(4):
        print(n)
