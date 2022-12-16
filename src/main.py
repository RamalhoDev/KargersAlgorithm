from KagerStructures import SuperNode
import random
from tqdm import tqdm
import pandas as pd
import plotly.express as px
import sys



def parse_graph(lines):
  n_vertices = int(lines[0])
  lines.pop(0)

  origin = 1
  edges = []

  for line in lines:
    split = line.split(' ')
    destination = 1
    for value in split:
      if value == '\n':
        continue
      adjacency = int(value)

      if adjacency == 1 and (destination, origin) not in edges:
        edges.append((origin, destination))
      destination = destination + 1
    origin = origin + 1

  vertices = [i for i in range(1, n_vertices + 1)]

  return {'vertices': vertices, 'edges': edges}

def find_vertex(id, supernodes: list):
  for supernode in supernodes:
    if id in supernode.nodes:
      return supernode
  return None


def merge(origin, destination, supernodes: list, superedges: list):
  origin_node = find_vertex(origin, supernodes)
  destination_node = find_vertex(destination, supernodes)

  _x = SuperNode(origin_node.nodes + destination_node.nodes)

  for _w in supernodes:
    if _w == origin_node or _w == destination_node:
      continue

    superedges[(_x, _w)] = superedges.get(
      (origin_node, _w), []) + superedges.get((destination_node, _w), [])

  return _x


def get_cut(supernodes, edges):
  _a = supernodes[0]
  _b = supernodes[1]
  cut = 0
  for vertex_a in _a.nodes:
    for vertex_b in _b.nodes:
      if (vertex_a, vertex_b) in edges or (vertex_b, vertex_a) in edges:
        cut = cut + 1
  return cut

def karger(graph):
  supernodes = [SuperNode([i]) for i in graph['vertices']]
  superedges = dict()

  for _u in supernodes:
    for _v in supernodes:
      if (_u.nodes[0], _v.nodes[0]) in graph['edges']:
        superedges[(_u, _v)] = [(_u.nodes[0], _v.nodes[0])]
      elif _u != _v:
        superedges[(_u, _v)] = []

  edges: list = graph['edges'].copy()

  while (len(supernodes) > 2):
    origin, destination = random.choice(edges)
    origin_node = find_vertex(origin, supernodes)
    if destination in origin_node.nodes:
      continue
    _x = merge(origin, destination, supernodes, superedges)

    edges_to_remove = superedges.get(
      (find_vertex(origin, supernodes), find_vertex(destination, supernodes)),
      []) + superedges.get((find_vertex(
        destination, supernodes), find_vertex(origin, supernodes)), [])
    edges = [i for i in edges if i not in edges_to_remove]

    supernodes.remove(find_vertex(origin, supernodes))
    supernodes.remove(find_vertex(destination, supernodes))
    supernodes.append(_x)


  return get_cut(supernodes, graph["edges"])


def naive_algorithm(graph):
  v = graph['vertices']
  edges = graph['edges']
  s = set(random.choices(v, k=random.randrange(1, len(v)-1)))
  v = set(v)
  s_bar = v - s
  cut = 0

  for i in s:
    for j in s_bar:
      if (i, j) in edges or (j,i) in edges:
        cut = cut + 1

  return cut

def run_iter(func, graph, iter):
    best = -1
    for i in range(iter):
        res = func(graph)
        if best == -1 or res < best:
            best = res
    return best


def main():
  instance = sys.argv[1]
  result = sys.argv[2]
  
  best_cut = 0
  with open(result) as f:
      best_cut = int(f.readline())
  print(best_cut)
  lines = ''
  with open(instance) as f:
    lines = f.readlines()
  
  graph = parse_graph(lines)
  
  count_best_karger = 0
  count_best_naive = 0
  
  percentage_karger = 0
  percentage_naive = 0
  iterations = 1
  
  data = {"percentages": [], "type":[], "iterations":[]}
  n_exec = 10000
  while(percentage_karger < 0.99):
      for i in tqdm(range(n_exec), desc= "Progresso"):
          best_karger = run_iter(karger, graph, iterations)
          best_naive = run_iter(naive_algorithm, graph, iterations)
  
          if best_karger == best_cut:
              count_best_karger = count_best_karger + 1
          if best_naive == best_cut:
              count_best_naive = count_best_naive + 1
  
      percentage_karger = count_best_karger/n_exec
      percentage_naive = count_best_naive/n_exec
      data["percentages"].append(percentage_karger)
      data["type"].append("karger")
      data["percentages"].append(percentage_naive)
      data["type"].append("naive")
      data["iterations"].append(iterations)
      data["iterations"].append(iterations)
      count_best_karger = 0
      count_best_naive = 0
      iterations = iterations * 2
  
  df = pd.DataFrame(data)
  fig = px.line(df, x="iterations", y="percentages", color="type", title='Análise Empírica Naive x Kargers', markers=True)
  fig.show()

if __name__=="__main__":
  main()
