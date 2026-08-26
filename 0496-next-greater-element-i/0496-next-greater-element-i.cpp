class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        std::vector<int> ans;
        std::stack<int>s;
        std::unordered_map<int,int> map;
        for(int i=0;i<nums2.size();++i){
            if(s.empty()||nums2[i]<s.top()){
                s.push(nums2[i]);
            }
            else if(nums2[i]>s.top()){
                while(!s.empty()&&s.top()<nums2[i]){
                    map.insert({s.top(),nums2[i]});
                    s.pop();
                    
                }
                s.push(nums2[i]);
            }
        }
        for(int i=0;i<nums1.size();i++){
            if(map[nums1[i]]>nums1[i]){
                ans.push_back(map[nums1[i]]);
            }
            else{
                ans.push_back(-1);
            }
        }
        return ans;
    }
};