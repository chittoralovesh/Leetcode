class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        mini=float('inf')
        ans=0

        for price in prices:
            mini=min(mini,price)

            ans=max(ans,price-mini)

        return ans