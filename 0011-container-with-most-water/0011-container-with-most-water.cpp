class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0;
        int r = height.size() - 1;
        int ans = 0;

        while (l < r) {
            int h = min(height[l], height[r]);
            int w = r - l;

            ans = max(ans, h * w);

            if (height[l] < height[r]) {
                l++;
            } else {
                r--;
            }
        }

        return ans;
    }
};