## Problem Description
Union-Find, also known as Disjoint Set, is a data structure that keeps track of a partition of a set into disjoint subsets. It provides two primary operations:

1. Union: Join two subsets into a single subset.
2. Find: Determine which subset a particular element is in. This operation returns an identifier for the subset.

Your task is to implement a Union-Find data structure that supports the above operations.

```
input:  [("union", 1, 2), ("union", 3, 4), ("find", 2), ("union", 2, 3), ("find", 4)]
output: [1, 1]
```