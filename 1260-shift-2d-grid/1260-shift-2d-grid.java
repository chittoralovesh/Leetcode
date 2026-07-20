class Solution {
    public List<List<Integer>> shiftGrid(int[][] grid, int k) {
        int m = grid.length;
        int n = grid[0].length;

        int[][] mat = new int[m][n];
        k = k % (m * n);

        for(int i=0; i<m; i++) {
            for(int j=0; j<n; j++) {
                int idx = i * n + j;
                int newIdx = (idx + k) % (m * n);

                int newRow = newIdx / n;
                int newCol = newIdx % n;

                mat[newRow][newCol] = grid[i][j];
            }
        }

        List<List<Integer>> res = new ArrayList<>();

        for(int i=0; i<m; i++) {
            List<Integer> list = new ArrayList<>();
            for(int j=0; j<n; j++) {
                list.add(mat[i][j]);
            }

            res.add(list);
        }

        return res;
    }
} 