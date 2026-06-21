from collections import defaultdict
from math import gcd

class Solution:
    def maxPoints(self, points):
        n = len(points)

        if n <= 2:
            return n

        ans = 1

        for i in range(n):
            slopes = defaultdict(int)

            for j in range(i + 1, n):
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]

                g = gcd(dx, dy)
                dx //= g
                dy //= g

                if dx < 0:
                    dx *= -1
                    dy *= -1
                elif dx == 0:
                    dy = 1
                elif dy == 0:
                    dx = 1

                slopes[(dy, dx)] += 1

            curr_max = 0
            for count in slopes.values():
                curr_max = max(curr_max, count)

            ans = max(ans, curr_max + 1)

        return ans