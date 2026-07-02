from collections import defaultdict, deque

class Solution:
    def minJumps(self, nums):
        n = len(nums)
        if n == 1:
            return 0

        mx = max(nums)

        # Smallest Prime Factor sieve
        spf = list(range(mx + 1))
        i = 2
        while i * i <= mx:
            if spf[i] == i:
                for j in range(i * i, mx + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        # prime -> indices divisible by prime
        primeToIndices = defaultdict(list)

        for idx, x in enumerate(nums):
            t = x
            while t > 1:
                p = spf[t]
                primeToIndices[p].append(idx)
                while t % p == 0:
                    t //= p

        q = deque([0])
        visited = [False] * n
        visited[0] = True

        usedPrime = set()
        steps = 0

        while q:
            for _ in range(len(q)):
                i = q.popleft()

                if i == n - 1:
                    return steps

                # adjacent left
                if i > 0 and not visited[i - 1]:
                    visited[i - 1] = True
                    q.append(i - 1)

                # adjacent right
                if i + 1 < n and not visited[i + 1]:
                    visited[i + 1] = True
                    q.append(i + 1)

                # teleport
                val = nums[i]
                if val > 1 and spf[val] == val and val not in usedPrime:
                    usedPrime.add(val)

                    for nxt in primeToIndices[val]:
                        if not visited[nxt]:
                            visited[nxt] = True
                            q.append(nxt)

            steps += 1

        return -1   