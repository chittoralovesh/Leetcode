class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        nums = [str(i) for i in range(1, n + 1)]

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        k -= 1  # Convert to 0-based indexing
        ans = []

        for i in range(n, 0, -1):
            idx = k // fact[i - 1]
            ans.append(nums.pop(idx))
            k %= fact[i - 1]

        return ''.join(ans)