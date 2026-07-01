from collections import deque

class Solution:
    def maximumSafenessFactor(self, grid):
        n = len(grid)

        # Step 1: Multi-source BFS to find distance from nearest thief
        dist = [[-1] * n for _ in range(n)]
        q = deque()

        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    dist[i][j] = 0
                    q.append((i, j))

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while q:
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

        # Check if a path exists with minimum distance >= val
        def can(val):
            if dist[0][0] < val:
                return False

            vis = [[False] * n for _ in range(n)]
            q = deque([(0, 0)])
            vis[0][0] = True

            while q:
                x, y = q.popleft()
                if x == n - 1 and y == n - 1:
                    return True

                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < n
                        and 0 <= ny < n
                        and not vis[nx][ny]
                        and dist[nx][ny] >= val
                    ):
                        vis[nx][ny] = True
                        q.append((nx, ny))

            return False

        lo, hi = 0, max(max(row) for row in dist)
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        return ans