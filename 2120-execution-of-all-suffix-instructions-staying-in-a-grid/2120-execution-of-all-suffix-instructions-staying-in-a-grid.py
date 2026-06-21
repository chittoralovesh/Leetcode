class Solution:
    def executeInstructions(self, n: int, startPos: List[int], s: str) -> List[int]:
        m = len(s)
        ans = [0] * m

        directions = {
            'L': (0, -1),
            'R': (0, 1),
            'U': (-1, 0),
            'D': (1, 0)
        }

        for i in range(m):
            row, col = startPos
            count = 0

            for j in range(i, m):
                dr, dc = directions[s[j]]
                nr, nc = row + dr, col + dc

                if not (0 <= nr < n and 0 <= nc < n):
                    break

                row, col = nr, nc
                count += 1

            ans[i] = count

        return ans