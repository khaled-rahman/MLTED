import os
import sys
from sets import Set
import Queue
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import numpy as np
import argparse

def generateLabels(labelSize):
	labels = []
	for i in range(labelSize):
		labels.append('l'+str(i+1))
	return labels

def generateNodes(nodeSize):
	nodes = []
	for i in range(nodeSize):
		nodes.append('n'+str(i+1))
	return nodes

def selectLabels(labels, n):
	selectedLabels = []
	for i in range(n):
		index = randint(0, len(labels) - 1)
		selectedLabels.append(labels[index])
		labels.remove(labels[index])
	return selectedLabels, labels

def assignLabelsToNode(labels, nodes):
	labeledNodes = []
	for i in range(len(nodes) - 1):
		perNodeLabels = randint(1, len(labels) / len(nodes))
		selectedLabels, labels = selectLabels(labels, perNodeLabels)
		labeledNodes.append(selectedLabels)
		nodes.remove(nodes[0])
	labeledNodes.append(labels)
	return labeledNodes

def createAdjacentList(nodes, mbf):
	
	Q = Queue.Queue()
	Q.put(nodes[0])
	nodes.remove(nodes[0])
	adjDict = dict()
	while len(nodes) > 0:
		node = Q.get()
		branch = randint(1, min(mbf, len(nodes)))
		children = []
		for i in range(branch):
			Q.put(nodes[0])
			children.append(nodes[0])
			nodes.remove(nodes[0])
		adjDict[node] = ",".join(children)

	return adjDict

def createTrees(labels, nodes, branchFactor, filename):
	l = generateLabels(labels)
	n = generateNodes(nodes)
	nodes = np.copy(n)
	sl = assignLabelsToNode(l, n)
	adjList = createAdjacentList(list(nodes), branchFactor)
	outfile = open("./trees/"+filename, "w")
	print sl
	print nodes
	print adjList
	for i in range(len(nodes)):
		outfile.write(nodes[i] + "=" + ",".join(sl[i]) + "\n")
	for i in adjList:
		outfile.write(i+ ":"+ adjList[i]+"\n")
	outfile.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Tree Generations', add_help=True)
	parser.add_argument('-n', '--n', required=True, type=str, help='Number of nodes')
	parser.add_argument('-l', '--l', required=True, type=str, help='Number of labels (should be greater than number of nodes)')
	parser.add_argument('-b', '--b', required=True, type=str, help='Maximum Branching Factor')
	parser.add_argument('-f', '--f', required=True, type=str, help='Filename without extension')
	args = parser.parse_args()
	n = args.n
	l = args.l
	f = args.f
	b = args.b
	createTrees(int(l), int(n), int(b), f+"1.txt")
	createTrees(int(l), int(n), int(b), f+"2.txt")
		

	

