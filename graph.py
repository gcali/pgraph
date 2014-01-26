#! /usr/bin/env python3

import sys
import subprocess
from random import seed, randint

from queue import Queue

def empty_fun(*args):
  pass

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

  def bfs_forest(self):
    
    visited = set()
    forest = []
    for node in self.nodes():
      if node not in visited:
        forest.append(self.bfs(node, visited, empty_fun))
    return forest

        

  def dfs(self, root, visited = set(), fun = print): 

    self._father = {}
    self._visited = visited

    self._visited.add(root)

    self._dfs_rec(root, fun)

    father = self._father

    self._father = {}
    self._visited = set()

    return create_tree(root, father)

  def dfs_forest(self):
    visited = set()
    forest = []
    for node in self.nodes():
      if node not in visited:
        forest.append(self.dfs(node, visited, empty_fun))
    return forest
        

  def _dfs_rec(self, root, fun):
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

def create_dot_graph(g_list, name_out):

  with subprocess.Popen(["dot", "-Tjpg", "-o", name_out],
                        stdin=subprocess.PIPE) as proc:
    proc.stdin.write(bytes("digraph {\n"\
                           "  rankdir=LR\n", "UTF-8"))
    for g in g_list:
      for node in g.nodes():
        proc.stdin.write(bytes("  {0} ;\n".format(node), "UTF-8"))
        for child in g.adj(node):
          proc.stdin.write(bytes("  {0} -> {1} ;\n".format(node, child), "UTF-8"))
    proc.stdin.write(bytes("}\n", "UTF-8"))
    


if __name__ == "__main__":
  if len(sys.argv) < 2:
    g = Graph()
    g.connect(0, 2)
    g.connect(0, 4)
    g.connect(2, 3)
    g.connect(3, 1)
    g.connect(3, 4)
    g.connect(1, 0)
    print(g)
  else: 
    seed()
    file_name = sys.argv[1]
    if len(sys.argv) >= 3:
      n_nodes = int(sys.argv[2])
    else:
      n_nodes = 10
    if len(sys.argv) >= 4:
      n_edges = int(sys.argv[3])
    else:
      n_edges = n_nodes * 3 // 2

    g = Graph()

    for i in range(n_nodes):
       g.create(i)

    for i in range(n_edges):
      source = randint(0,n_nodes-1)
      dest = randint(0,n_nodes-1)
      g.connect(source, dest)

    create_dot_graph([g], file_name + "_orig.jpg")
    forest = g.dfs_forest()
    create_dot_graph(forest, file_name + "_dfs.jpg")
    create_dot_graph([g.bfs(0, fun=empty_fun)], file_name + "_bfs.jpg")
