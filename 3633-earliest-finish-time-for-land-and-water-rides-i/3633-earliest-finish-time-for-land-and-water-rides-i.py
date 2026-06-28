class Solution:
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
        ans = float('inf')

        n = len(landStartTime)
        m = len(waterStartTime)

        for i in range(n):
            for j in range(m):
                # Land -> Water
                finish_land = landStartTime[i] + landDuration[i]
                start_water = max(finish_land, waterStartTime[j])
                ans = min(ans, start_water + waterDuration[j])

                # Water -> Land
                finish_water = waterStartTime[j] + waterDuration[j]
                start_land = max(finish_water, landStartTime[i])
                ans = min(ans, start_land + landDuration[i])

        return ans