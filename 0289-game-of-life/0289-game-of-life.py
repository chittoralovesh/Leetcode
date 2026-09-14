from typing import List

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        n, m = len(board), len(board[0])
        
        # Directions for neighbors
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # First pass: **Mark** temporary state changes
        for i in range(n):
            for j in range(m):
                live_neighbors = 0
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    
                    if 0 <= ni < n and 0 <= nj < m:
                        # Check if neighbor was originally live
                        if board[ni][nj] in [1, 2]:
                            live_neighbors += 1

                if board[i][j] == 1: # Current cell is live
                    if live_neighbors < 2 or live_neighbors > 3:
                        board[i][j] = 2 # live -> dead
                else: # Current cell is dead
                    if live_neighbors == 3:
                        board[i][j] = 3 # dead -> live

        # Second pass: **Finalize** state changes
        for i in range(n):
            for j in range(m):
                if board[i][j] == 2:
                    board[i][j] = 0 # Finalize live -> dead
                elif board[i][j] == 3:
                    board[i][j] = 1 # Finalize dead -> live