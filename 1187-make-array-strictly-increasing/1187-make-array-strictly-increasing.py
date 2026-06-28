from bisect import bisect_right

class Solution:
    def makeArrayIncreasing(self, arr1, arr2):
        arr2 = sorted(set(arr2))

        # dp[last_value] = minimum operations
        dp = {-1: 0}

        for num in arr1:
            new_dp = {}

            for prev, ops in dp.items():

                # Option 1: Keep current element
                if num > prev:
                    if num not in new_dp or new_dp[num] > ops:
                        new_dp[num] = ops

                # Option 2: Replace with smallest valid value from arr2
                idx = bisect_right(arr2, prev)
                if idx < len(arr2):
                    replace = arr2[idx]
                    if replace not in new_dp or new_dp[replace] > ops + 1:
                        new_dp[replace] = ops + 1

            if not new_dp:
                return -1

            dp = new_dp

        return min(dp.values())     