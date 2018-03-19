import os
import sys
from sets import Set
import Queue
import networkx as nx
import matplotlib.pyplot as plt


def createParentChildren(line):
	parent = line.strip().split(":")[0]
	children = line.strip().replace(" ","").split(":")[1].split(",")
	return parent, children

def createLabels(line):
	node = line.strip().split("=")[0].replace(" ", "")
	labels = line.strip().replace(" ","").split("=")[1].split(",")
	return node, labels


def SAP(S, T):
	Tab = [[0 for i in range(len(S))] for j in range(len(T))]
	for i in range(len(S)):
		Tab[i][0] = 0
	for j in range(len(T)):
		Tab[0][j] = 0
	for i in range(1, len(S)):
		for j in range(1, len(T)):
			Tab[i][j] = max(Tab[i-1][j], Tab[i][j-1])+len(list(set(S[i]).intersection(set(T[j]))))
	#for r in Tab:
	#	print r
	return Tab

def PWAT(nS, nT, S, T, Sparent, Tparent):
	patDict = dict()
	bfsOrderT1 = []
	bfsOrderT2 = []
	Q1 = Queue.Queue()
	parent1 = S.iterkeys().next()
	Q1.put(parent1)
	Q2 = Queue.Queue()
	parent2 = T.iterkeys().next()
	Q2.put(parent2)

	while not Q1.empty():
		p1 = Q1.get()
		bfsOrderT1.append(p1)
		if p1 not in S:
			continue
		for c1 in S[p1]:
			Q1.put(c1)
	while not Q2.empty():
		p2 = Q2.get()
		bfsOrderT2.append(p2)
		if p2 not in T:
			continue
		for c2 in T[p2]:
			Q2.put(c2)

	for a in bfsOrderT1:
		Q1 = Queue.Queue()
		Q1.put(a)
		while not Q1.empty():
			b = Q1.get()
			for c in bfsOrderT2:
				Q2 = Queue.Queue()
				Q2.put(c)
				while not Q2.empty():
					d = Q2.get()
					#print 'Node:',a, b, c, d
					if a == b and c == d:
						patDict["".join(a+b+c+d)] = len(list(set(nS[b]).intersection(set(nT[d]))))
					elif a == b and c != d:
						patDict["".join(a+b+c+d)] = patDict["".join(a+b+c+Tparent[d])] + len(list(set(nS[b]).intersection(set(nT[d]))))
					elif a != b and c == d:
						patDict["".join(a+b+c+d)] = patDict["".join(a+Sparent[b]+c+d)] + len(list(set(nS[b]).intersection(set(nT[d]))))
					else:
						patDict["".join(a+b+c+d)] = max(patDict["".join(a+b+c+Tparent[d])], patDict["".join(a+Sparent[b]+c+d)]) + len(list(set(nS[b]).intersection(set(nT[d]))))
					if d not in T:
						continue
					for c2 in T[d]:
						Q2.put(c2)
			if b not in S:
				continue
			for c1 in S[b]:
				Q1.put(c1)
	#print patDict
	return patDict


def readTreeFile(pathToFile):
	assert os.path.exists(pathToFile), "There does not exist file " + pathToFile + ". Function readlabelsAncestryMatrix"
	treeFile = open(pathToFile)
	nodes = dict()
	labels = []
	adjList = dict()
	parentList = dict()
	for line in treeFile.readlines():
		if "=" in line:
			n, l = createLabels(line)
			nodes[n] = l
			labels.append(l)
		elif ":" in line:
			p, c = createParentChildren(line)
			adjList[p] = c
			for label in c:
				parentList[label] = p
	treeFile.close()
	return labels, nodes, adjList, parentList

def createGraph(nodes, edges, cost):
	G = nx.DiGraph()
	for i in nodes:
		G.add_node(i)
	for e in range(len(edges)):
		i = edges[e][0]
		j = edges[e][1]
		w = cost[e]
		G.add_edge(i,j, weight = w, capacity = 1)

def findLCA(node1, node2, T1parent):

	nV1 = []
	nV2 = []

	while node1 in T1parent.keys():
		nV1.append(node1)
		node1 = T1parent[node1]
	nV1.append(node1)
	print nV1

	while node2 in T2parent.keys():
		nV2.append(node2)
		node2 = T2parent[node2]
	nV2.append(node2)
	nV1[:] = nV1[::-1]
	nV2[:] = nV2[::-1]
	for i in range(min(len(nV1), len(nV2))):
		if nV1[i] == nV2[i]:
			lca = nV1[i]
		else:
			break
	print lca

	return lca

if __name__ == '__main__':
	if len(sys.argv) == 3:
		l1, n1, T1adj, T1parent = readTreeFile(sys.argv[1])
		l2, n2, T2adj, T2parent = readTreeFile(sys.argv[2])
		#print l1
		#print n1
		#print T1adj
		#print T1parent
		sap = SAP(l1, l2)
		pwat = PWAT(n1, n2, T1adj, T2adj, T1parent, T2parent)
		lca = findLCA('F', 'E', T1parent)
		#print sap
		#print pwat
		

	

