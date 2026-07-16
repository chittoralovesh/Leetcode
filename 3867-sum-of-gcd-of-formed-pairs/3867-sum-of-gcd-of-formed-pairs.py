from typing import List
from math import gcd

class Solution:
    def gcdSum(self, nums: List[int]) -> int:
        prefixGcd = []
        mx = 0

        for x in nums:
            mx = max(mx, x)
            prefixGcd.append(gcd(x, mx))

        prefixGcd.sort()

        ans = 0
        n = len(prefixGcd)
        for i in range(n // 2):
            ans += gcd(prefixGcd[i], prefixGcd[n - 1 - i])

        return ans