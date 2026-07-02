class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, l, r):
            if not node:
                return True
            if not l < node.val < r:
                return False
            return dfs(node.left, l, node.val) and dfs(node.right, node.val, r)

        return dfs(root, float("-inf"), float("inf"))   