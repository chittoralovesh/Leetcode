class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        
        1. the idea is to flip rows (row 0 elements with row 2 elements if it's a 3x3 matrix; row 0 with row 3 and row 1 with row 2 if it's a 4x4 matrix)
        
        2. then swap elements a[i][j] = a[j][i]
        
        *edge* think of a 1x1 matrix which has only 1 element 
        *remember* this is a symmetric matrix (n x n )
        
        """
        if not matrix:
            return []
        rows = len(matrix)
        cols = len(matrix[0])
        
        # flip rows
        top = 0
        bottom = rows - 1
        while top < bottom:
            for col in range(cols):
                matrix[top][col], matrix[bottom][col] = matrix[bottom][col], matrix[top][col]
            top += 1
            bottom -= 1
        
        # swap elements
        for row in range(rows):
            for col in range(cols):
                if row < col: # if we don't add this check we are swapping elements twice and end up with the same matrix
                    matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]
        return matrix