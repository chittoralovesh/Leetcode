from functools import lru_cache

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int,
                  startRow: int, startColumn: int) -> int:

        MOD = 10**9 + 7

        @lru_cache(None)
        def dfs(row, col, moves):
            if row < 0 or row >= m or col < 0 or col >= n:
                return 1

            if moves == 0:
                return 0

            return (
                dfs(row + 1, col, moves - 1) +
                dfs(row - 1, col, moves - 1) +
                dfs(row, col + 1, moves - 1) +
                dfs(row, col - 1, moves - 1)
            ) % MOD

        return dfs(startRow, startColumn, maxMove)