# de Bruijn assembly option
import argparse
import networkx as nx
parser = argparse.ArgumentParser()
parser.add_argument('reads')
args = parser.parse_args()

with open(args.reads) as reads_fh:
  reads = reads_fh.read().splitlines()

def edgeMap(edges):
    maps = {}
    for edge in edges:
        i = edge[0]
        if i not in maps:
          maps[i] = [edge[1]]
        else:
          maps[i].append(edge[1])
    return maps


def eulerianWalks(m,s):
    maps = m
    start = s
    result = [start]
    while(1):
        pre = start
        path = []
        while(1):
            if pre in maps:
              nextNode = maps[pre].pop()
              if len(maps[pre]) == 0:
                  maps.pop(pre)
              path.append(nextNode)
              if nextNode != start:
                  pre = nextNode
              else:
                break    
            else:
              break
        result = result[:result.index(start)+1] + path + result[result.index(start)+1:len(result)]
        if len(maps) == 0:
          break
        newStart = False
        for i in result:
            if i in maps:
                start = i
                newStart = True
                break
        if newStart == False:
            break
    return result


def main():
  graph = nx.MultiDiGraph()

  for line in reads:
      L = line[:-1]
      R = line[1:]
      graph.add_node(L)
      graph.add_node(R)
      graph.add_edge(L, R)

  getOddDegree = []
  for odd in graph.degree():
      if odd[1] % 2 != 0:
          getOddDegree.append(odd)
  
  if graph.in_degree(getOddDegree[1][0]) > graph.out_degree(getOddDegree[1][0]) :
    start = getOddDegree[0][0]
  else:
    start = getOddDegree[1][0]

  maps = edgeMap(graph.edges)
  t = eulerianWalks(maps,start)
  if len(set(t)) != len(graph.nodes):
    print(-1)
    return
  result = t[0][:-1]
  for n in t:
    result += n[-1]
  print(result)

main()
