class Solution:
    def countDigitOne(self, n: int) -> int:
        ans = 0
        m = 1

        while m <= n:
            high = n // (m * 10)
            cur = (n // m) % 10
            low = n % m

            if cur == 0:
                ans += high * m
            elif cur == 1:
                ans += high * m + low + 1
            else:
                ans += (high + 1) * m

            m *= 10

        return ans      