from node import Node
from vectors import Vct
import config

def getMasterNode():
    file = open(".session")
    stream = list(map(str.strip, file.readlines()))
    masterNode = Node(Vct(0,0), 0, "master")

    while len(stream) > 0:
        child = parseLine(stream)
        masterNode.childs.append(child)

    return masterNode

def parseLine(stream, depth = 0):
    line = stream.pop(0)

    tokens = line.split(";")
    name = tokens[0]
    pos = Vct.fromTuple(list(map(float, tokens[1].split(","))))
    childs = int(tokens[2])
    node = Node(pos, config.defaultRadius * depth**config.scaler, name) 

    for _ in range(childs):
        child = parseLine(stream, depth+1)
        node.childs.append(child)

    return node


