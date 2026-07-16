from typing import List

class Solution:
    def checkRecord(self, n: int) -> int:
        MOD = 10**9 + 7

        dp = [[0] * 3 for _ in range(2)]
        dp[0][0] = 1

        for _ in range(n):
            ndp = [[0] * 3 for _ in range(2)]

            for a in range(2):
                for l in range(3):
                    if dp[a][l] == 0:
                        continue

                    # Add 'P'
                    ndp[a][0] = (ndp[a][0] + dp[a][l]) % MOD

                    # Add 'A'
                    if a == 0:
                        ndp[1][0] = (ndp[1][0] + dp[a][l]) % MOD

                    # Add 'L'
                    if l < 2:
                        ndp[a][l + 1] = (ndp[a][l + 1] + dp[a][l]) % MOD

            dp = ndp

        return sum(sum(row) for row in dp) % MOD