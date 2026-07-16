from typing import List

class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        m, n = len(mat), len(mat[0])
        ans = []

        for d in range(m + n - 1):
            temp = []

            r = 0 if d < n else d - n + 1
            c = d if d < n else n - 1

            while r < m and c >= 0:
                temp.append(mat[r][c])
                r += 1
                c -= 1

            if d % 2 == 0:
                ans.extend(temp[::-1])
            else:
                ans.extend(temp)

        return ans