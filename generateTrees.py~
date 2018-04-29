import os
import sys
from sets import Set
import Queue
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
	outfile = open(filename, "w")
	for i in range(len(nodes)):
		outfile.write(nodes[i] + "=" + ",".join(sl[i]) + "\n")
	for i in adjList:
		outfile.write(i+ ":"+ adjList[i]+"\n")
	outfile.close()
	return sl, nodes, adjList

def findIn2D(array, element):
	arr = [arr for arr in array if element in arr][0]
	x = array.index(arr)
	y = arr.index(element)
	return x,y

def findRelation(node1, node2, adj):
	#print adj
	relation = -1
	if node1 not in adj and node2 not in adj:
		return 0
	else:
		flag = 0
		Q = Queue.Queue()
		#print node1
		Q.put(node1)
		while not Q.empty():
			tmpNode = Q.get()
			#print tmpNode
			if tmpNode == node2:
				relation = 1
				flag = 1
				break
			if tmpNode not in adj:
				continue
			for c in adj[tmpNode]:
				#print 'Children:', c
				Q.put(c)
		#print flag, relation
		
		if flag == 1 and relation == 1:
			return 1
		else:
			return 2

def createParentChildren(line):
	parent = line.strip().split(":")[0]
	children = line.strip().replace(" ","").split(":")[1].split(",")
	return parent, children

def makeIterableAdjList(adj):
	adjList = dict()
	allkeys = adj.keys()
	for k in allkeys:
		line = str(k + ":" + adj[k])
		p, c = createParentChildren(line)
		adjList[p] = c
	return adjList

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
	l1, n1, adj1 = createTrees(int(l), int(n), int(b), f+"1.txt")
	l2, n2, adj2 = createTrees(int(l), int(n), int(b), f+"2.txt")
	adj11 = makeIterableAdjList(adj1)
	adj21 = makeIterableAdjList(adj2)
	
		

	

