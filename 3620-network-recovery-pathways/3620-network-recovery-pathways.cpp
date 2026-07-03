class Solution {
public:
    int findMaxPathScore(vector<vector<int>>& edges, vector<bool>& online, long long k) {
        int n = online.size();

        vector<vector<pair<int,int>>> adj(n);
        vector<int> indeg(n,0);
        vector<int> vals;

        for(auto &e:edges){
            adj[e[0]].push_back({e[1],e[2]});
            indeg[e[1]]++;
            vals.push_back(e[2]);
        }

        // Topological order
        queue<int> q;
        for(int i=0;i<n;i++)
            if(indeg[i]==0) q.push(i);

        vector<int> topo;
        while(!q.empty()){
            int u=q.front(); q.pop();
            topo.push_back(u);
            for(auto &[v,w]:adj[u]){
                if(--indeg[v]==0)
                    q.push(v);
            }
        }

        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());

        auto check = [&](int limit)->bool{
            const long long INF = (1LL<<60);
            vector<long long> dist(n, INF);
            dist[0]=0;

            for(int u:topo){
                if(dist[u]==INF) continue;

                // intermediate offline nodes cannot be used
                if(u!=0 && u!=n-1 && !online[u]) continue;

                for(auto &[v,w]:adj[u]){
                    if(w<limit) continue;

                    if(v!=n-1 && v!=0 && !online[v]) continue;

                    if(dist[v] > dist[u] + w)
                        dist[v] = dist[u] + w;
                }
            }

            return dist[n-1] <= k;
        };

        int lo=0, hi=vals.size()-1;
        int ans=-1;

        while(lo<=hi){
            int mid=(lo+hi)/2;

            if(check(vals[mid])){
                ans=vals[mid];
                lo=mid+1;
            }else{
                hi=mid-1;
            }
        }

        return ans;
    }
};