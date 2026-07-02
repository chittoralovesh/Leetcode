class Solution:
    def isRectangleCover(self, rectangles: List[List[int]]) -> bool:
        s=set()
        area=0
        x1=y1=10**9
        x2=y2=-10**9

        for a,b,c,d in rectangles:
            x1=min(x1,a)
            y1=min(y1,b)
            x2=max(x2,c)
            y2=max(y2,d)
            area+=(c-a)*(d-b)

            for p in ((a,b),(a,d),(c,b),(c,d)):
                if p in s:s.remove(p)
                else:s.add(p)

        return area==(x2-x1)*(y2-y1) and s=={
            (x1,y1),(x1,y2),(x2,y1),(x2,y2)
        }      