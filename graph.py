#! /usr/bin/env python3

import sys

from queue import Queue

class Graph(dict):
  def connect(self,a,b):
    self.create(a)
    self.create(b)

    if b not in self[a]:
      self[a].append(b)
      self[a].sort()
  def create(self,a):
    if a not in self.keys():
      self[a] = []

  def adj(self,node):
    return self[node]

  def nodes(self):
    return [node for node in sorted(self.keys())]

  def bfs(self, root, visited = set(), fun = print):
    
    queue = Queue()
    father = {}

    visited.add(root)
    queue.put(root)

    while not queue.empty():
      node = queue.get()
      for child in self.adj(node):
        if child not in visited:
          visited.add(child)
          father[child] = node
          queue.put(child)
      fun(node)

    return create_tree(node, father)

  def dfs(self, root, visited = set(), fun = print): 

    self._father = {}
    self._visited = visited

    self._visited.add(root)

    self._dfs_rec(root, fun)

    father = self._father

    self._father = {}
    self._visited = set()

    return create_tree(root, father)

  def _dfs_rec(self, root, fun = print):
    fun(root)
    for child in self.adj(root):
      if child not in self._visited:
        self._visited.add(child)
        self._father[child] = root
        self._dfs_rec(child, fun)
    

          
def create_tree(root, father):
  g = Graph()
  g.create(root)
  for (c,f) in father.items():
    g.connect(f,c)

  return g

def create_dot_graph(g, out):
  print(r"digraph {", file=out)
  for node in g.nodes():
    for child in g.adj(node):
      print(r"  {0} -> {1} ;".format(node, child), file=out)
  print(r"}", file=out)
    


if __name__ == "__main__":
  if not sys.argv:
    exit(1)
  else:
    g = Graph()
    g.connect(0, 2)
    g.connect(0, 4)
    g.connect(2, 3)
    g.connect(3, 1)
    g.connect(3, 4)
    g.connect(1, 0)
  with open("data.gv", "w") as f:
    create_dot_graph(g.bfs(0), f)
  with open("dfs.gv", "w") as f:
    create_dot_graph(g.dfs(0), f)
