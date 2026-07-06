class Solution:
    def champagneTower(self, poured, query_row, query_glass):
        dp = [[0.0] * (r + 1) for r in range(102)]
        dp[0][0] = float(poured)

        for r in range(query_row + 1):
            for c in range(r + 1):
                if dp[r][c] > 1.0:
                    overflow = (dp[r][c] - 1.0) / 2.0
                    dp[r + 1][c] += overflow
                    dp[r + 1][c + 1] += overflow

        return min(1.0, dp[query_row][query_glass])