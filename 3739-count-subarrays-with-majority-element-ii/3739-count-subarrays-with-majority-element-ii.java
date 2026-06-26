import java.util.*;

class Solution {
    class Fenwick {
        int[] bit;

        Fenwick(int n) {
            bit = new int[n + 2];
        }

        void update(int idx, int val) {
            while (idx < bit.length) {
                bit[idx] += val;
                idx += idx & -idx;
            }
        }

        int query(int idx) {
            int sum = 0;
            while (idx > 0) {
                sum += bit[idx];
                idx -= idx & -idx;
            }
            return sum;
        }
    }

    public long countMajoritySubarrays(int[] nums, int target) {
        int n = nums.length;

        int[] pref = new int[n + 1];

        for (int i = 0; i < n; i++) {
            pref[i + 1] = pref[i] + (nums[i] == target ? 1 : -1);
        }

        int[] vals = pref.clone();
        Arrays.sort(vals);

        HashMap<Integer, Integer> map = new HashMap<>();
        int idx = 1;
        for (int v : vals) {
            if (!map.containsKey(v)) {
                map.put(v, idx++);
            }
        }

        Fenwick bit = new Fenwick(idx);

        long ans = 0;

        for (int x : pref) {
            int id = map.get(x);
            ans += bit.query(id - 1);
            bit.update(id, 1);
        }

        return ans;
    }
}