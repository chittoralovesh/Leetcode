from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        g = defaultdict(list)
        for a, b in sorted(tickets, reverse=True):
            g[a].append(b)

        ans = []

        def dfs(u):
            while g[u]:
                dfs(g[u].pop())
            ans.append(u)

        dfs("JFK")
        return ans[::-1]    