class Solution {
public:
    long long solveOrder(vector<int>& startA, vector<int>& durA,
                         vector<int>& startB, vector<int>& durB) {

        int m = startB.size();

        vector<pair<long long,long long>> ridesB;
        for (int i = 0; i < m; i++) {
            ridesB.push_back({startB[i], durB[i]});
        }

        sort(ridesB.begin(), ridesB.end());

        vector<long long> starts(m);
        vector<long long> suffixStartPlusDur(m);

        for (int i = 0; i < m; i++) {
            starts[i] = ridesB[i].first;
        }

        suffixStartPlusDur[m - 1] =
            ridesB[m - 1].first + ridesB[m - 1].second;

        for (int i = m - 2; i >= 0; i--) {
            suffixStartPlusDur[i] =
                min(suffixStartPlusDur[i + 1],
                    ridesB[i].first + ridesB[i].second);
        }

        vector<long long> prefixMinDur(m);
        prefixMinDur[0] = ridesB[0].second;

        for (int i = 1; i < m; i++) {
            prefixMinDur[i] =
                min(prefixMinDur[i - 1], ridesB[i].second);
        }

        long long ans = LLONG_MAX;

        for (int i = 0; i < startA.size(); i++) {

            long long finishA =
                (long long)startA[i] + durA[i];

            int pos =
                upper_bound(starts.begin(), starts.end(), finishA)
                - starts.begin();

            long long best = LLONG_MAX;

            // rides already open
            if (pos > 0) {
                best = min(best,
                           finishA + prefixMinDur[pos - 1]);
            }

            // rides not yet open
            if (pos < m) {
                best = min(best,
                           suffixStartPlusDur[pos]);
            }

            ans = min(ans, best);
        }

        return ans;
    }

    int earliestFinishTime(vector<int>& landStartTime,
                           vector<int>& landDuration,
                           vector<int>& waterStartTime,
                           vector<int>& waterDuration) {

        long long ans1 =
            solveOrder(landStartTime, landDuration,
                       waterStartTime, waterDuration);

        long long ans2 =
            solveOrder(waterStartTime, waterDuration,
                       landStartTime, landDuration);

        return (int)min(ans1, ans2);
    }
};