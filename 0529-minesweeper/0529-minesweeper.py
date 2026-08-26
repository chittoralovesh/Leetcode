class Solution:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        m, n = len(board), len(board[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1), (-1, -1), (1, 1)]

        def dfs(i, j):
            if board[i][j] == "M":
                board[i][j] = "X"
                return

            mines = 0
            for i_off, j_off in directions:
                r, c = i + i_off, j + j_off
                if 0 <= r < m and 0 <= c < n and board[r][c] == "M":
                    mines += 1
            if mines > 0:
                board[i][j] = str(mines)
            else:
                board[i][j] = "B"
                for i_off, j_off in directions:
                    r, c = i + i_off, j + j_off
                    if 0 <= r < m and 0 <= c < n:
                        if board[r][c] == "E":
                            dfs(r, c)

        dfs(click[0], click[1])
        return board