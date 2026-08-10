class Solution:
    # 0 = Not calculated
    # 1 = Alice
    # 2 = Bob
    def winnerSquareGame(self, n):
        self.memo = [[0] * 2 for _ in range(n + 1)]
        return self.game(n, True)

    def game(self, n, isAlice):
        isAliceIdx = 1 if isAlice else 0
        if self.memo[n][isAliceIdx] != 0:
            return self.memo[n][isAliceIdx] == 1
        c = 1
        best = not isAlice
        i = 1
        while c <= n:
            if not isAlice:
                if not self.game(n - c, True):
                    best = False
                    break
            else:
                if self.game(n - c, False):
                    best = True
                    break
            i += 1
            c = i * i
        self.memo[n][isAliceIdx] = 1 if best else 2
        return best