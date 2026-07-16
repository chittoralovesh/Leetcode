from typing import List

class Solution:
    def judgePoint24(self, cards: List[int]) -> bool:
        EPS = 1e-6

        def dfs(nums):
            if len(nums) == 1:
                return abs(nums[0] - 24) < EPS

            n = len(nums)

            for i in range(n):
                for j in range(i + 1, n):
                    a, b = nums[i], nums[j]
                    rest = [nums[k] for k in range(n) if k != i and k != j]

                    candidates = [
                        a + b,
                        a - b,
                        b - a,
                        a * b,
                    ]

                    if abs(b) > EPS:
                        candidates.append(a / b)
                    if abs(a) > EPS:
                        candidates.append(b / a)

                    for x in candidates:
                        if dfs(rest + [x]):
                            return True

            return False

        return dfs([float(x) for x in cards])