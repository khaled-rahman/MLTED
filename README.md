# How to run/use:
Users need to check out the following instructions. We provide both Python and C++ implementations.

## Tree Structure
We represent trees in the following way:

```
Root=Label1,Label2, ...
Node1=Label3,Label4, ...
Node2=Label5,Label6, ...
Root:Node1,Node2
```
Each line of input contains either '=' or ':'. If a line contains '=', it means that left side of this sign represents a node and right side of it represents set of assigned labels to this node. If a line contains ':', it means that left side of it contains a node of the tree and right side of it contains children of that node (similar to adjacent list). First line that contains ':', represents the root node and its corresponding children. 

Check t1.txt file for an example. t1.txt, t2.txt, t3.txt and t4.txt are example trees in the paper which represent Reference Tree, Tree 1, Tree 2 and Tree 3, respectively. N.B. Do not put a blank line in the tree file.

## Python
install munkres package for maximum bipartite matching as follows:
```
pip install munkres --user
```

To run leafDelTED.py, type the following command:
```
python leafDelTED.py t1.txt t2.txt
```

Output will be similarity and distance values.

## C++
To run main.cpp, type the following command:
```
g++ -std=c++11 main.cpp -o main
./main t1.txt t2.txt
```
Output will be similarity and distance values.

## Generate Random Trees
To generate random pair trees, run generateTrees.py as follows:
```
python generateTrees.py -n 10 -l 20 -b 3 -f test
```

Here,
```
n - specifies number of nodes which is 10
l - specifies number of labels that will be distributed among n nodes, which is 20
b - specifies highest number of branching factor which is 3
f - specifies prefix of two output files' name. Here, test means two output files will be test1.txt and test2.txt
```

## Citation

If you use this for any reason, please cite our paper.

