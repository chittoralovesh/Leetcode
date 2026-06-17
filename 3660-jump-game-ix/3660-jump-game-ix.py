from typing import List

class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)

        prefix_max = [0] * n
        suffix_min = [0] * n

        prefix_max[0] = nums[0]
        for i in range(1, n):
            prefix_max[i] = max(prefix_max[i - 1], nums[i])

        suffix_min[n - 1] = nums[n - 1]
        for i in range(n - 2, -1, -1):
            suffix_min[i] = min(suffix_min[i + 1], nums[i])

        ans = [0] * n

        start = 0
        comp_max = nums[0]

        for i in range(n):
            comp_max = max(comp_max, nums[i])

            end_component = (
                i == n - 1 or
                prefix_max[i] <= suffix_min[i + 1]
            )

            if end_component:
                for j in range(start, i + 1):
                    ans[j] = comp_max

                start = i + 1
                if start < n:
                    comp_max = nums[start]

        return ans      