# The guess API is already defined for you.
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        l, r = 1, n
        while l <= r:
            m = (l + r) // 2
            x = guess(m)
            if x == 0:
                return m
            if x < 0:
                r = m - 1
            else:
                l = m + 1