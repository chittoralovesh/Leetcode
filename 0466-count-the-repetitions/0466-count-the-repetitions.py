from typing import List

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0

        recall = {}
        s2_index = 0
        s2_count = 0

        s1_count = 0

        while s1_count < n1:
            s1_count += 1

            for ch in s1:
                if ch == s2[s2_index]:
                    s2_index += 1
                    if s2_index == len(s2):
                        s2_index = 0
                        s2_count += 1

            if s2_index in recall:
                prev_s1_count, prev_s2_count = recall[s2_index]

                cycle_s1 = s1_count - prev_s1_count
                cycle_s2 = s2_count - prev_s2_count

                remain = n1 - s1_count
                times = remain // cycle_s1

                s1_count += times * cycle_s1
                s2_count += times * cycle_s2
            else:
                recall[s2_index] = (s1_count, s2_count)

        return s2_count // n2    