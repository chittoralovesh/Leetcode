class Solution {
public:
    struct Event {
        long long y;
        int type;
        long long x1, x2;

        bool operator<(const Event& other) const {
            return y < other.y;
        }
    };

    struct SegmentTree {
        vector<int> cnt;
        vector<long long> len;
        vector<long long> xs;

        SegmentTree(const vector<long long>& coords) {
            xs = coords;
            int n = xs.size();
            cnt.assign(4 * n, 0);
            len.assign(4 * n, 0);
        }

        void pushUp(int node, int l, int r) {
            if (cnt[node] > 0) {
                len[node] = xs[r + 1] - xs[l];
            } else if (l == r) {
                len[node] = 0;
            } else {
                len[node] = len[node * 2] + len[node * 2 + 1];
            }
        }

        void update(int node, int l, int r,
                    int ql, int qr, int val) {

            if (ql > r || qr < l) return;

            if (ql <= l && r <= qr) {
                cnt[node] += val;
                pushUp(node, l, r);
                return;
            }

            int mid = (l + r) >> 1;

            update(node * 2, l, mid, ql, qr, val);
            update(node * 2 + 1, mid + 1, r, ql, qr, val);

            pushUp(node, l, r);
        }

        long long coveredLength() {
            return len[1];
        }
    };

    double separateSquares(vector<vector<int>>& squares) {

        vector<Event> events;
        vector<long long> xs;

        for (auto &s : squares) {
            long long x = s[0];
            long long y = s[1];
            long long l = s[2];

            events.push_back({y, 1, x, x + l});
            events.push_back({y + l, -1, x, x + l});

            xs.push_back(x);
            xs.push_back(x + l);
        }

        sort(xs.begin(), xs.end());
        xs.erase(unique(xs.begin(), xs.end()), xs.end());

        sort(events.begin(), events.end());

        SegmentTree st(xs);

        vector<tuple<long long,long long,long long>> strips;
        // (y1, y2, coveredWidth)

        long long prevY = events[0].y;
        long long width = 0;

        int m = xs.size();

        for (int i = 0; i < (int)events.size(); ) {

            long long curY = events[i].y;

            if (curY > prevY) {
                strips.push_back({prevY, curY, width});
            }

            while (i < (int)events.size() &&
                   events[i].y == curY) {

                int l = lower_bound(xs.begin(), xs.end(),
                                    events[i].x1) - xs.begin();

                int r = lower_bound(xs.begin(), xs.end(),
                                    events[i].x2) - xs.begin();

                st.update(
                    1,
                    0,
                    m - 2,
                    l,
                    r - 1,
                    events[i].type
                );

                i++;
            }

            width = st.coveredLength();
            prevY = curY;
        }

        long double totalArea = 0;

        for (auto &[y1, y2, w] : strips) {
            totalArea += (long double)(y2 - y1) * w;
        }

        long double target = totalArea / 2.0;

        long double areaSoFar = 0;

        for (auto &[y1, y2, w] : strips) {

            long double stripArea =
                (long double)(y2 - y1) * w;

            if (areaSoFar + stripArea >= target) {

                long double remain =
                    target - areaSoFar;

                return (double)(y1 +
                       remain / (long double)w);
            }

            areaSoFar += stripArea;
        }

        return 0.0;
    }
};