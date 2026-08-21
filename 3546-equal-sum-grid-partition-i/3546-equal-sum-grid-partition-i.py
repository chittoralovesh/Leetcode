class Solution:
    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        sum = [[0] * (n + 1) for _ in range(m + 1)]
        total = 0
        for i in range(m):
            for j in range(n):
                sum[i + 1][j + 1] = (
                    sum[i + 1][j] + sum[i][j + 1] - sum[i][j] + grid[i][j]
                )
                total += grid[i][j]
        for i in range(m - 1):
            if total == sum[i + 1][n] * 2:
                return True
        for i in range(n - 1):
            if total == sum[m][i + 1] * 2:
                return True
        return False