import os
import sys
from sets import Set
import Queue
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
					if a == b and c == d:
						patDict["".join(a+c+b+d)] = len(list(set(nS[b]).intersection(set(nT[d]))))
					elif a == b and c != d:
						patDict["".join(a+c+b+d)] = patDict["".join(a+c+b+Tparent[d])] + len(list(set(nS[b]).intersection(set(nT[d]))))
					elif a != b and c == d:
						patDict["".join(a+c+b+d)] = patDict["".join(a+c+Sparent[b]+d)] + len(list(set(nS[b]).intersection(set(nT[d]))))
					else:
						patDict["".join(a+c+b+d)] = max(patDict["".join(a+c+b+Tparent[d])], patDict["".join(a+c+Sparent[b]+d)]) + len(list(set(nS[b]).intersection(set(nT[d]))))
					if d not in T:
						continue
					for c2 in T[d]:
						Q2.put(c2)
			if b not in S:
				continue
			for c1 in S[b]:
				Q1.put(c1)
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

def improveMatching(v):
    u = T[v]
    if u in Mu:
        improveMatching(Mu[u])
    Mu[u] = v
    Mv[v] = u

def augmentPath():
    while True:
        ((val, u), v) = min([(minSlack[v], v) for v in V if v not in T])
        assert u in S
        if val>0:        
           	for i in S:
        		lu[i] -= val
    		for j in V:
        		if j in T:
        			lv[j] += val
        		else:
        			minSlack[j][0] -= val
        assert lu[u]+lv[v]-w[u][v]==0
        T[v] = u                          
        if v in Mv:
            u1 = Mv[v]                     
            assert not u1 in S
            S[u1] = True                 
            for v in V:                  
                if not v in T and minSlack[v][0] > lu[u1]+lv[v]-w[u1][v]:
                    minSlack[v] = [lu[u1]+lv[v]-w[u1][v], u1]
        else:
            improveMatching(v)          
            return

def maxBipartiteMatching(weights):
	#Kuhn Munkres @hungarian algorithm
	#https://pypi.python.org/pypi/munkres/1.0.5.4
    global U,V,S,T,Mu,Mv,lu,lv, minSlack, w
    w  = weights
    n  = len(w)
    U  = V = range(n)
    lu = [ max([w[u][v] for v in V]) for u in U]
    lv = [ 0                         for v in V]
    Mu = {}                                      
    Mv = {}
    while len(Mu)<n:
        free = [u for u in V if u not in Mu]     
        u0 = free[0]
        S = {u0: True}                  
        T = {}
        minSlack = [[lu[u0]+lv[v]-w[u0][v], u0] for v in V]
        augmentPath()
    val = sum(lu)+sum(lv)
    return (Mu, Mv, val)


def optimalMatching(nS, nT, S, T, Sparent, Tparent, pwat):
	G = dict()
	dfsOrderT1 = []
	dfsOrderT2 = []
	STACK1 = []
	parent1 = S.iterkeys().next()
	STACK1.append(parent1)
	STACK2 = []
	parent2 = T.iterkeys().next()
	STACK2.append(parent2)
	visited = []
	while len(STACK1) > 0:
		p1 = STACK1[len(STACK1) - 1]
		if p1 not in S or p1 in visited:
			dfsOrderT1.append(p1)
			STACK1.pop()
			continue
		visited.append(p1)
		for c1 in S[p1]:
			STACK1.append(c1)
	visited = []
	while len(STACK2) > 0:
		p2 = STACK2[len(STACK2) - 1]
		if p2 not in T or p2 in visited:
			dfsOrderT2.append(p2)
			STACK2.pop()
			continue
		visited.append(p2)
		for c2 in T[p2]:
			STACK2.append(c2)
	print dfsOrderT1
	print dfsOrderT2
	for n1 in dfsOrderT1:
		F = []
		if n1 in S:
			F = [i for i in S[n1]]
		for n2 in dfsOrderT2:
			H = []
			if n2 in T:
				H = [j for j in T[n2]]
			#print n1, n2, ":", F, H
			if len(F) == 0 and len(H) == 0:
				G["".join(n1+n2)] = pwat["".join(n1+n2+n1+n2)]
			elif len(F) == 0 and len(H) != 0:
				for c in H:
					if "".join(n1+n2) in G:
						if pwat["".join(n1+n2+n1+c)] > G["".join(n1+n2)]:
							G["".join(n1+n2)] =  pwat["".join(n1+n2+n1+c)]
					else:
						G["".join(n1+n2)] = pwat["".join(n1+n2+n1+c)]
			elif len(F) != 0 and len(H) == 0:
				for c in F:
					if "".join(n1+n2) in G:
						if pwat["".join(n1+n2+c+n2)] > G["".join(n1+n2)]:
							G["".join(n1+n2)] = pwat["".join(n1+n2+c+n2)]
					else:
						G["".join(n1+n2)] = pwat["".join(n1+n2+c+n2)]
			else:
				Cost = []
				for c1 in F:
					nodesofSubtreec1 = []
					subQ1 = Queue.Queue()
					subQ1.put(c1)
					while not subQ1.empty():
						sn1 = subQ1.get()
						nodesofSubtreec1.append(sn1)
						if sn1 not in S:
							continue
						for subc1 in S[sn1]:
							subQ1.put(subc1)
					subCost = []
					for c2 in H:
						nodesofSubtreec2 = []
						subQ2 = Queue.Queue()
						subQ2.put(c2)
						while not subQ2.empty():
							sn2 = subQ2.get()
							nodesofSubtreec2.append(sn2)
							if sn2 not in T:
								continue
							for subc2 in T[sn2]:
								subQ2.put(subc2)
						# if "".join(n1+n2) in G:
						# 	if pwat["".join(n1+n2+c1+c2)] + G["".join(c1+c2)] > G["".join(c1+c2)]:
						# 		G["".join(n1+n2)] = pwat["".join(n1+n2+c1+c2)] + G["".join(c1+c2)]
						# else:
						# 	G["".join(n1+n2)] = pwat["".join(n1+n2+c1+c2)] + G["".join(c1+c2)]
						allCost = []
						for c in nodesofSubtreec1:
							for d in nodesofSubtreec2:
								allCost.append(pwat["".join(c1+c2+c+d)] + G["".join(c+d)])
						#bG["".join(c1+c2)] = max(allCost)
						subCost.append(max(allCost))
					Cost.append(subCost)
				print F, H
				print Cost
				(n,n, val) = maxBipartiteMatching(Cost)
				G["".join(n1+n2)] = val
				print val
								
	print G

	return G

if __name__ == '__main__':
	if len(sys.argv) == 3:
		l1, n1, T1adj, T1parent = readTreeFile(sys.argv[1])
		l2, n2, T2adj, T2parent = readTreeFile(sys.argv[2])
		#print l1
		#print n1
		#print T1adj
		#print T1parent
		#sap = SAP(l1, l2)
		pwat = PWAT(n1, n2, T1adj, T2adj, T1parent, T2parent)
		#print pwat
		#lca = findLCA('F', 'E', T1parent)
		#print sap
		#print pwat
		dfs = optimalMatching(n1, n2, T1adj, T2adj, T1parent, T2parent, pwat)
		vals = dfs.values()
		print "Output:", max(vals)
		#print dfs
		

	

