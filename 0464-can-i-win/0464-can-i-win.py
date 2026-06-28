from functools import cache

class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        # If target is already reached
        if desiredTotal <= 0:
            return True

        # Sum of all numbers is not enough
        total = maxChoosableInteger * (maxChoosableInteger + 1) // 2
        if total < desiredTotal:
            return False

        @cache
        def dfs(mask, remaining):
            # Try every unused number
            for num in range(1, maxChoosableInteger + 1):
                bit = 1 << (num - 1)

                # Skip if already used
                if mask & bit:
                    continue

                # Win immediately
                if num >= remaining:
                    return True

                # If opponent loses, current player wins
                if not dfs(mask | bit, remaining - num):
                    return True

            # No winning move
            return False

        return dfs(0, desiredTotal)