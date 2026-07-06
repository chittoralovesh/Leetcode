from typing import List

class Solution:
    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0

        for i in range(n):
            even = {}
            odd = {}
            de = 0
            do = 0

            for j in range(i, n):
                x = nums[j]

                if x % 2 == 0:
                    if x not in even:
                        even[x] = 1
                        de += 1
                    else:
                        even[x] += 1
                else:
                    if x not in odd:
                        odd[x] = 1
                        do += 1
                    else:
                        odd[x] += 1

                if de == do:
                    ans = max(ans, j - i + 1)

        return ans