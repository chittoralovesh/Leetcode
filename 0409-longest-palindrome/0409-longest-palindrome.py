from collections import Counter

class Solution:
    def longestPalindrome(self, s: str) -> int:
        ans = 0

        for freq in Counter(s).values():
            ans += freq // 2 * 2

            if ans % 2 == 0 and freq % 2 == 1:
                ans += 1

        return ans