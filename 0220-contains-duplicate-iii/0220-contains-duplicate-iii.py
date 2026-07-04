from typing import List

class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        if valueDiff < 0:
            return False

        bucket = {}
        size = valueDiff + 1

        for i, num in enumerate(nums):
            bucket_id = num // size      # No extra adjustment!

            if bucket_id in bucket:
                return True

            if bucket_id - 1 in bucket and abs(num - bucket[bucket_id - 1]) <= valueDiff:
                return True

            if bucket_id + 1 in bucket and abs(num - bucket[bucket_id + 1]) <= valueDiff:
                return True

            bucket[bucket_id] = num

            if i >= indexDiff:
                old = nums[i - indexDiff]
                del bucket[old // size]

        return False