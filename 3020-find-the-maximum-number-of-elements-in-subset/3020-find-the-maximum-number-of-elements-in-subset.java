class Solution {
    public int maximumLength(int[] nums) {
        HashMap<Long, Integer> freq = new HashMap<>();

        for (int x : nums) {
            freq.put((long) x, freq.getOrDefault((long) x, 0) + 1);
        }

        int ans = 1;

        // Special handling for 1
        if (freq.containsKey(1L)) {
            int c = freq.get(1L);
            ans = Math.max(ans, (c % 2 == 0) ? c - 1 : c);
        }

        for (long x : freq.keySet()) {
            if (x == 1) continue;

            long cur = x;
            int len = 0;

            while (freq.getOrDefault(cur, 0) >= 2) {
                len += 2;
                if (cur > (long) 1e9) break;
                cur = cur * cur;
                if (cur > (long) 1e18 / Math.max(1, cur)) break;
            }

            if (freq.getOrDefault(cur, 0) >= 1)
                len++;
            else
                len--;

            ans = Math.max(ans, len);
        }

        return ans;
    }
}