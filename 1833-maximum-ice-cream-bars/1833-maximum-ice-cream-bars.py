class Solution:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        freq = [0] * 100001

        for c in costs:
            freq[c] += 1

        bars = 0

        for cost in range(1, 100001):
            if freq[cost] == 0:
                continue

            buy = min(freq[cost], coins // cost)

            bars += buy
            coins -= buy * cost

            if coins == 0:
                break

        return bars