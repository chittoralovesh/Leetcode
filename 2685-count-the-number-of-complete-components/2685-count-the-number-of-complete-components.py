from typing import List

class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            pa, pb = find(a), find(b)
            if pa != pb:
                parent[pb] = pa

        for u, v in edges:
            union(u, v)

        comp = {}
        for i in range(n):
            r = find(i)
            if r not in comp:
                comp[r] = [0, 0]   # [vertices, degree_sum]
            comp[r][0] += 1

        for u, v in edges:
            r = find(u)
            comp[r][1] += 2

        ans = 0
        for vertices, degree_sum in comp.values():
            if degree_sum == vertices * (vertices - 1):
                ans += 1

        return ans