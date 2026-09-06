class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        
        def getStateAfterTransfer(state, leftToRight):
            idx_of_sender = 0 if leftToRight else -1
            idx_of_receiver = idx_of_sender + 1
            # Check what the max capcity of the receiving jug is
            max_capacity_receiver = y if leftToRight else x
            space_in_receiver = max_capacity_receiver - state[idx_of_receiver]
            # You can only transfer until the receiver jug becomes full or sender jug empties out.
            transfer_amount = min(space_in_receiver, state[idx_of_sender])
            
            # convert to list because tuples are immutable
            state_list = list(state)
            state_list[idx_of_sender] = state_list[idx_of_sender] - transfer_amount
            state_list[idx_of_receiver] = state_list[idx_of_receiver] + transfer_amount
            return tuple(state_list)

        
        seen = set()

        queue = deque([(0, 0), (0, y), (x, 0), (x, y)])
        while queue:
            state = queue.popleft()
            if state[0] + state[1] == target:
                return True
            if state in seen:
                continue
            seen.add(state)
            queue.append((state[0], y))
            queue.append((x, state[1]))
            queue.append((0, state[1]))
            queue.append((state[0], 0))
            queue.append(getStateAfterTransfer(state, True))
            queue.append(getStateAfterTransfer(state, False))
        return False