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

def SED(S, T):
	Tab = [[0 for i in range(len(S))] for j in range(len(T))]
	for i in range(len(S)):
		Tab[0][i] = 0
		Tab[i][0] = 0
	for i in range(len(S)-1):
		for j in range(len(T)-1):
			Tab[i+1][j] = max(Tab[i+1][j], Tab[i][j]+len(list(set(S[i]).intersection(set(T[j])))))
			Tab[i][j+1] = max(Tab[i][j+1], Tab[i][j]+len(list(set(S[i]).intersection(set(T[j])))))
	print Tab
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
		SED(l1, l2)

	

