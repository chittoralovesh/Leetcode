class Solution {
public:
    struct Node {
        long long cnt;
        long long wav;
    };

    string s;
    Node dp[20][11][11][3][2];
    bool vis[20][11][11][3][2];

    Node dfs(int pos, int p2, int p1, int lenState, bool started, bool tight) {
        if (pos == (int)s.size()) {
            return {1, 0};
        }

        if (!tight && vis[pos][p2][p1][lenState][started]) {
            return dp[pos][p2][p1][lenState][started];
        }

        int limit = tight ? (s[pos] - '0') : 9;

        long long totalCnt = 0;
        long long totalWav = 0;

        for (int d = 0; d <= limit; d++) {
            bool ntight = tight && (d == limit);

            if (!started && d == 0) {
                Node child = dfs(pos + 1, 10, 10, 0, false, ntight);

                totalCnt += child.cnt;
                totalWav += child.wav;
            } else {
                int contrib = 0;

                if (lenState >= 2) {
                    if ((p1 > p2 && p1 > d) || (p1 < p2 && p1 < d)) {
                        contrib = 1;
                    }
                }

                int np2, np1, nlen;

                if (lenState == 0) {
                    np2 = 10;
                    np1 = d;
                    nlen = 1;
                } else if (lenState == 1) {
                    np2 = p1;
                    np1 = d;
                    nlen = 2;
                } else {
                    np2 = p1;
                    np1 = d;
                    nlen = 2;
                }

                Node child = dfs(pos + 1, np2, np1, nlen, true, ntight);

                totalCnt += child.cnt;
                totalWav += child.wav + 1LL * contrib * child.cnt;
            }
        }

        Node res = {totalCnt, totalWav};

        if (!tight) {
            vis[pos][p2][p1][lenState][started] = true;
            dp[pos][p2][p1][lenState][started] = res;
        }

        return res;
    }

    long long solve(long long n) {
        if (n <= 0) return 0;

        s = to_string(n);
        memset(vis, 0, sizeof(vis));

        return dfs(0, 10, 10, 0, false, true).wav;
    }

    long long totalWaviness(long long num1, long long num2) {
        return solve(num2) - solve(num1 - 1);
    }
};