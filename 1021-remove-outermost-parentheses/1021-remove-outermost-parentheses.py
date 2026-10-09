class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        stack = []
        answer = []

        for c in s:
            if c == '(':
                if stack:
                    answer.append(c)
                stack.append(c)
            else:
                stack.pop()
                if stack:
                    answer.append(c)

        return ''.join(answer)