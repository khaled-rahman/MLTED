import os
import sys
from sets import Set
import Queue


def createParentChildren(line):
	parent = line.strip().split(":")[0]
	children = line.strip().replace(" ","").split(":")[1].split(",")
	return parent, children

def createLabels(line):
	node = line.strip().split("=")[0]
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
	for r in Tab:
		print r
def readTreeFile(pathToFile):
	assert os.path.exists(pathToFile), "There does not exist file " + pathToFile + ". Function readlabelsAncestryMatrix"
	treeFile = open(pathToFile)
	nodes = dict()
	labels = []
	adjList = dict()
	for line in treeFile.readlines():
		if "=" in line:
			n, l = createLabels(line)
			nodes[n] = l
			labels.append(l)
		elif ":" in line:
			p, c = createParentChildren(line)
			adjList[p] = c
	treeFile.close()
	return labels, nodes, adjList

	
if __name__ == '__main__':
	if len(sys.argv) == 3:
		l1, n1, T2 = readTreeFile(sys.argv[1])
		l2, n2, T2 = readTreeFile(sys.argv[2])
		SAP(l1, l2)

	

