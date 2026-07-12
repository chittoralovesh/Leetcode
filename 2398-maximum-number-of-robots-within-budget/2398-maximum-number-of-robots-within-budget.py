from collections import deque

class Solution:
    def maximumRobots(self, chargeTimes, runningCosts, budget):
        dq = deque()      # stores indices, chargeTimes in decreasing order
        left = 0
        run_sum = 0
        ans = 0

        for right in range(len(chargeTimes)):
            run_sum += runningCosts[right]

            while dq and chargeTimes[dq[-1]] <= chargeTimes[right]:
                dq.pop()
            dq.append(right)

            while dq and chargeTimes[dq[0]] + (right - left + 1) * run_sum > budget:
                if dq[0] == left:
                    dq.popleft()
                run_sum -= runningCosts[left]
                left += 1

            ans = max(ans, right - left + 1)

        return ans