from node import Node
from vectors import Vct
import config

def getMasterNode():
    file = open(".session", 'r')
    stream = list(map(str.strip, file.readlines()))
    masterNode = Node(Vct(0,0), 0, "master")

    while len(stream) > 0:
        child = parseLine(stream)
        masterNode.childs.append(child)

    file.close()

    return masterNode

def parseLine(stream, depth = 0):
    line = stream.pop(0)

    tokens = line.split(";")
    name = tokens[0]
    pos = Vct.fromTuple(list(map(float, tokens[1].split(","))))
    childs = int(tokens[2])
    node = Node(pos, config.defaultRadius * config.scaler**depth, name) 

    for _ in range(childs):
        child = parseLine(stream, depth+1)
        node.childs.append(child)

    return node

def on_exit(master_node):
    file = open(".session", 'w')
    
    for child in master_node.childs:
        dump_node(child, file)

    file.close()

def dump_node(node, file):
    file.write(f"{node.name};{int(node.pos.x)},{int(node.pos.y)};{len(node.childs)}\n")

    for child in node.childs:
        dump_node(child, file)

