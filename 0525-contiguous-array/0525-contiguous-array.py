from typing import List

class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        prefix = 0
        first = {0: -1}
        ans = 0

        for i, x in enumerate(nums):
            if x == 0:
                prefix -= 1
            else:
                prefix += 1

            if prefix in first:
                ans = max(ans, i - first[prefix])
            else:
                first[prefix] = i

        return ans