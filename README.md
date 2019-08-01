# A multi-labeled tree dissimilarity measure for comparing "clonal trees" of tumor progression

# How to run/use:
Users need to check out the following instructions. We provide C++ implementation.

## Tree Structure
We represent trees in the following way:

```
Root=Label1,Label2, ...
Node1=Label3,Label4, ...
Node2=Label5,Label6, ...
Root:Node1,Node2
```
Each line of input contains either '=' or ':'. If a line contains '=', it means that left side of this sign represents a node and right side of it represents set of assigned labels to this node. If a line contains ':', it means that left side of it contains a node of the tree and right side of it contains children of that node (similar to adjacent list). First line that contains ':', represents the root node and its corresponding children. 

Check t1.txt file for an example. t1.txt, t2.txt, t3.txt and t4.txt are example trees used in the paper which represent 'true tree', 'inferred ree 1', 'inferred tree 2' and 'inferred tree 3', respectively. **N.B. Do not put a blank line in the tree file.**

## C++
To run main.cpp, type the following command:
```
g++ -std=c++11 main.cpp -o main
./main t1.txt t2.txt
```
Output will distance value, similarity value and normalized similarity value. For the above example, output will be following:

```
Distance = 14
Similarity = 3
Normalized Similarity = 0.3
```

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

## Citations:
If you find this tool helpful in your work, please cite the followings:
```
@article{karpov2019multi,
  title={A multi-labeled tree dissimilarity measure for comparing “clonal trees” of tumor progression},
  author={Karpov, Nikolai and Malikic, Salem and Rahman, Md Khaledur and Sahinalp, S Cenk},
  journal={Algorithms for Molecular Biology},
  volume={14},
  number={1},
  pages={17},
  year={2019},
  publisher={Springer}
}
@inproceedings{karpov2018multi,
  title={A Multi-labeled Tree Edit Distance for Comparing" Clonal Trees" of Tumor Progression},
  author={Karpov, Nikolai and Malikic, Salem and Rahman, Md and Sahinalp, S Cenk and others},
  booktitle={18th International Workshop on Algorithms in Bioinformatics (WABI 2018)},
  year={2018},
  organization={Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik}
}
```

If you have questions/comments, please don't hesitate to email me at `morahma@iu.edu`.
