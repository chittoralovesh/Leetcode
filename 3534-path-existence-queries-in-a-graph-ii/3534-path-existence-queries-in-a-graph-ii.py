from bisect import bisect_right
from typing import List

class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[int]:
        order = sorted((nums[i], i) for i in range(n))

        val = [x for x, _ in order]
        idx = [i for _, i in order]

        pos = [0] * n
        for i, v in enumerate(idx):
            pos[v] = i

        # component id
        comp = [0] * n
        cid = 0
        comp[0] = 0
        for i in range(1, n):
            if val[i] - val[i - 1] > maxDiff:
                cid += 1
            comp[i] = cid

        LOG = 17
        nxt = [[0] * n for _ in range(LOG)]

        j = 0
        for i in range(n):
            while j + 1 < n and val[j + 1] - val[i] <= maxDiff:
                j += 1
            nxt[0][i] = j

        for k in range(1, LOG):
            for i in range(n):
                nxt[k][i] = nxt[k - 1][nxt[k - 1][i]]

        ans = []

        for u, v in queries:
            a = pos[u]
            b = pos[v]

            if comp[a] != comp[b]:
                ans.append(-1)
                continue

            if a > b:
                a, b = b, a

            if a == b:
                ans.append(0)
                continue

            cur = a
            steps = 0

            for k in range(LOG - 1, -1, -1):
                if nxt[k][cur] < b:
                    cur = nxt[k][cur]
                    steps += 1 << k

            ans.append(steps + 1)

        return ans  