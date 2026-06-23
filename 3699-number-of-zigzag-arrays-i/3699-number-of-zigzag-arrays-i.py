class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 10**9 + 7
        m = r - l + 1

        # Length = 2
        up = [0] * (m + 1)
        down = [0] * (m + 1)

        for v in range(1, m + 1):
            up[v] = v - 1          # previous value < v
            down[v] = m - v        # previous value > v

        for _ in range(3, n + 1):
            prefix_up = [0] * (m + 1)
            prefix_down = [0] * (m + 1)

            for v in range(1, m + 1):
                prefix_up[v] = (prefix_up[v - 1] + up[v]) % MOD
                prefix_down[v] = (prefix_down[v - 1] + down[v]) % MOD

            total_up = prefix_up[m]

            new_up = [0] * (m + 1)
            new_down = [0] * (m + 1)

            for v in range(1, m + 1):
                # Last move is up => previous move must be down
                new_up[v] = prefix_down[v - 1]

                # Last move is down => previous move must be up
                new_down[v] = (total_up - prefix_up[v]) % MOD

            up, down = new_up, new_down

        return (sum(up) + sum(down)) % MOD