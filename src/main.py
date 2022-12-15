from KagerStructures import SuperNode
import random

instance = "in/graph_type2_3"

lines = ''
with open(instance) as f:
  lines = f.readlines()


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

  supernodes[0].nodes.sort()
  supernodes[1].nodes.sort()
  # print(supernodes[0].nodes, supernodes[1].nodes, get_cut(supernodes, graph["edges"]))


def naive_algorithm(graph):
  v = graph['vertices']
  edges = graph['edges']
  s = set(random.choices(v, k=random.randrange(0, len(v)-1)))
  v = set(v)
  s_bar = v - s
  cut = 0
  for i in range(len(s)):
    for j in range(len(s_bar)):
      if (i, j) in edges:
        cut = cut + 1
  print(cut)


graph = parse_graph(lines)
karger(graph)
naive_algorithm(graph)
# print(graph)
