class Solution:
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:
        if not ops:
            return m * n

        min_row = m
        min_col = n

        for a, b in ops:
            min_row = min(min_row, a)
            min_col = min(min_col, b)

        return min_row * min_col