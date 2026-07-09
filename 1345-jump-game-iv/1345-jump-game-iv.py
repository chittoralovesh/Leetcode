from collections import defaultdict, deque
from typing import List

class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n == 1:
            return 0

        graph = defaultdict(list)
        for i, v in enumerate(arr):
            graph[v].append(i)

        q = deque([0])
        visited = [False] * n
        visited[0] = True
        steps = 0

        while q:
            for _ in range(len(q)):
                i = q.popleft()

                if i == n - 1:
                    return steps

                # Jump to all indices with the same value
                for j in graph[arr[i]]:
                    if not visited[j]:
                        visited[j] = True
                        q.append(j)

                # Process this value only once
                graph[arr[i]].clear()

                # Jump to i - 1
                if i - 1 >= 0 and not visited[i - 1]:
                    visited[i - 1] = True
                    q.append(i - 1)

                # Jump to i + 1
                if i + 1 < n and not visited[i + 1]:
                    visited[i + 1] = True
                    q.append(i + 1)

            steps += 1

        return -1