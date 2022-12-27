from static.tools import directions


class BusStation:
    def __init__(self, ID: int, name: str, direction: int):
        self.ID: int = ID
        self.name: str = name
        self.direction: str = directions[direction]


class Bus:
    def __init__(self, ID: int, route_number: int, start: int):
        self.ID: int = ID
        self.route_number: int = route_number
        #self.start: int = start


class Interval:
    def __init__(self, ID: int, station1: int, station2: int, timing: int):
        self.ID: int = ID
        self.station1: int = station1
        self.station2: int = station2
        self.interval: int = timing


class Route:
    def __init__(self, number: str, stations, full_round: int):
        self.number: str = number
        self.stations: list = stations
        self.full_round: int = full_round


class CloselyRoute:
    def __init__(self, number: str, minute: int):
        self.number: str = number
        self.minute: int = minute
