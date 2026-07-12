from collections import deque

class RideSharingSystem:

    def __init__(self):
        self.riders = deque()
        self.drivers = deque()
        self.waiting = set()
        self.cancelled = set()

    def addRider(self, riderId: int) -> None:
        self.riders.append(riderId)
        self.waiting.add(riderId)

    def addDriver(self, driverId: int) -> None:
        self.drivers.append(driverId)

    def matchDriverWithRider(self) -> list[int]:
        while self.riders and self.riders[0] in self.cancelled:
            rider = self.riders.popleft()
            self.cancelled.remove(rider)
            self.waiting.remove(rider)

        if not self.riders or not self.drivers:
            return [-1, -1]

        driver = self.drivers.popleft()
        rider = self.riders.popleft()
        self.waiting.remove(rider)
        return [driver, rider]

    def cancelRider(self, riderId: int) -> None:
        if riderId in self.waiting:
            self.cancelled.add(riderId)